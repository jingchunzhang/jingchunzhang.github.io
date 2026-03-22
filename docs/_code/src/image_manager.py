import os
import yaml
import re
import argparse
import sys
import glob
import json
import time
import requests
import shutil
from pathlib import Path
from typing import Optional, List, Set, Dict

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 配置文件路径 (相对于项目根目录)
CONFIG_FILE = PROJECT_ROOT / '_data' / 'image_config.yml'
HISTORY_FILE = PROJECT_ROOT / '_data' / 'image_history.yml'
LOCAL_IMAGE_DIR = PROJECT_ROOT / 'assets' / 'images' / 'generated'

DEFAULT_IMAGE = 'photo-1579684385127-1ef15d508118'

class ImageManager:
    """Manages image selection and generation to avoid duplicates."""
    
    def __init__(self, config_path=CONFIG_FILE):
        self.config = self.load_config(config_path)
        self.history = self.load_history()
        self.unsplash_key = self.config.get('unsplash', {}).get('access_key') or os.environ.get('UNSPLASH_ACCESS_KEY')
        self.volcengine_key = self.config.get('volcengine', {}).get('api_key') or os.environ.get('ARK_API_KEY')
        
        self.download_dir = str(LOCAL_IMAGE_DIR)
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        
        self.unsplash_requests_count = 0
        self.unsplash_limit = self.config.get('unsplash', {}).get('max_requests', 40)
        
        # 内存中跟踪本次会话使用过的图片
        self.session_used_ids: Set[str] = set()

    def load_config(self, path):
        if not os.path.exists(path):
            print(f"Config file not found: {path}")
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def load_history(self):
        if not os.path.exists(HISTORY_FILE):
            return {}
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(self.history, f, default_flow_style=False)

    def get_image(self, keywords: str) -> Optional[Dict[str, str]]:
        strategy = self.config.get('strategy', 'mixed')
        new_image = None
        
        unsplash_limit_hit = self.unsplash_requests_count >= self.unsplash_limit
        if strategy in ['unsplash', 'mixed'] and not unsplash_limit_hit:
            new_image = self.search_unsplash(keywords)
            if new_image:
                if 'used_unsplash_ids' not in self.history:
                    self.history['used_unsplash_ids'] = []
                self.history['used_unsplash_ids'].append(new_image['id'])
                self.session_used_ids.add(new_image['id'])
                self.save_history() 
                return new_image
        
        force_fallback = (strategy == 'unsplash' and unsplash_limit_hit)
        if not new_image and (strategy in ['volcengine', 'mixed'] or force_fallback):
            if unsplash_limit_hit and strategy == 'unsplash':
                 print(f"Forcing Volcengine fallback due to Unsplash limit ({self.unsplash_limit})")
            new_image = self.generate_volcengine(keywords)
            if new_image:
                 return new_image

        return None

    def search_unsplash(self, query):
        if not self.unsplash_key:
            return None
        
        if self.unsplash_requests_count >= self.unsplash_limit:
            return None
            
        self.unsplash_requests_count += 1

        url = "https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {self.unsplash_key}"}
        params = {
            "query": query,
            "per_page": 20, # 获取多一些用于去重
            "orientation": self.config.get('unsplash', {}).get('orientation', 'landscape')
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            used_ids = set(self.history.get('used_unsplash_ids', []))
            used_ids.update(self.session_used_ids)
            
            for result in data.get('results', []):
                image_id = result['id']
                # 使用 full URL 参数以确保一致性
                image_url = f"{result['urls']['regular']}?auto=format&fit=crop&w=1600&q=80"
                
                if image_id not in used_ids:
                    return {
                        'id': image_id,
                        'url': image_url,
                        'source': 'unsplash',
                        'credit': result['user']['name']
                    }
            
            # 如果这页都用过了，尝试随机取一个 (或者后续考虑翻页，目前简单处理)
            print(f"Warning: All Unsplash images for '{query}' already used.")
            
        except Exception as e:
            print(f"Unsplash API error: {e}")
        
        return None

    def generate_volcengine(self, prompt):
        if not self.volcengine_key:
            print("Volcengine API Key missing. Skipping generation.")
            return None

        print(f"Generating image with Volcengine: {prompt[:50]}...")
        
        url = self.config['volcengine']['api_url']
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.volcengine_key}"
        }
        
        prefix = self.config['volcengine'].get('prompt_prefix', '')
        full_prompt = f"{prefix}{prompt}"
        
        payload = {
            "model": self.config['volcengine']['model'],
            "prompt": full_prompt,
            "response_format": "url",
            "size": self.config['volcengine'].get('size', '1024x1024'),
            "guidance_scale": self.config['volcengine'].get('guidance_scale', 3),
            "logo_info": {
                "add_logo": False
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                image_url = data['data'][0]['url']
                
                # 下载到本地
                filename = f"gen_{int(time.time())}_{hash(prompt) % 10000}.png"
                local_path = os.path.join(self.download_dir, filename)
                
                img_data = requests.get(image_url, timeout=30).content
                with open(local_path, 'wb') as f:
                    f.write(img_data)
                
                print(f"Image downloaded to {local_path}")
                
                # 返回相对路径 (用于 Jekyll)
                # 假设 _site 构建时 assets 在根目录
                return {
                    'url': f"/assets/images/generated/{filename}", 
                    'source': 'volcengine',
                    'prompt': full_prompt
                }
            else:
                print(f"Unexpected API response: {data}")

        except Exception as e:
            print(f"Volcengine API error: {e}")
        
        return None

    def get_placeholder_pattern(self) -> str:
        """Return regex pattern for image placeholders."""
        return r'!\[IMAGE_PLACEHOLDER\]\((.*?)\)'

# Singleton instance
image_manager = ImageManager()

