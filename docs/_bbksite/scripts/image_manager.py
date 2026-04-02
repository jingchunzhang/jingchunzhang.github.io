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

BLOG_DIR = 'blog'
CONFIG_FILE = '_data/image_config.yml'
HISTORY_FILE = '_data/image_history.yml'
DEFAULT_IMAGE = 'photo-1579684385127-1ef15d508118'

class ImageManager:
    def __init__(self, config_path=CONFIG_FILE):
        self.config = self.load_config(config_path)
        self.history = self.load_history()
        self.unsplash_key = self.config.get('unsplash', {}).get('access_key') or os.environ.get('UNSPLASH_ACCESS_KEY')
        self.volcengine_key = self.config.get('volcengine', {}).get('api_key') or os.environ.get('ARK_API_KEY')
        
        self.download_dir = self.config.get('local_image_dir', 'assets/images/generated')
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        
        self.unsplash_requests_count = 0
        self.unsplash_limit = self.config.get('unsplash', {}).get('max_requests', 50)

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

    def get_frontmatter(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
            if match:
                return yaml.safe_load(match.group(1)), match.group(2), match.group(1)
            return {}, content, ""
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return {}, None, None

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
            "per_page": 10, 
            "orientation": self.config.get('unsplash', {}).get('orientation', 'landscape')
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            for result in data.get('results', []):
                image_id = result['id']
                image_url = result['urls']['regular']
                
                if image_id not in self.history.get('used_unsplash_ids', []):
                    return {
                        'id': image_id,
                        'url': image_url,
                        'source': 'unsplash',
                        'credit': result['user']['name']
                    }
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
            "watermark": True
        }

        response = None
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                image_url = data['data'][0]['url']
                
                filename = f"gen_{int(time.time())}_{hash(prompt) % 1000}.png"
                local_path = os.path.join(self.download_dir, filename)
                
                img_data = requests.get(image_url).content
                with open(local_path, 'wb') as f:
                    f.write(img_data)
                
                print(f"Image downloaded to {local_path}")
                
                return {
                    'url': f"/{local_path}", 
                    'source': 'volcengine',
                    'prompt': full_prompt
                }
            else:
                print(f"Unexpected API response: {data}")

        except Exception as e:
            print(f"Volcengine API error: {e}")
            if response:
                print(response.text)
        
        return None

    def process_file(self, filepath, dry_run=False):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return

        if DEFAULT_IMAGE not in content and 'source.unsplash.com' not in content:
            return
            
        print(f"Processing {filepath}...")
        
        fm, _, _ = self.get_frontmatter(filepath)
        title = fm.get('title', '')
        tags = fm.get('tags', [])
        if isinstance(tags, str): tags = [tags]
        
        keywords = f"{title} {' '.join(tags[:3])}"
        keywords = keywords.replace('"', '').replace("'", "").strip()
        if not keywords:
            keywords = "diabetes health lifestyle" 
        
        strategy = self.config.get('strategy', 'mixed')
        new_image = None
        
        unsplash_limit_hit = self.unsplash_requests_count >= self.unsplash_limit
        
        if strategy in ['unsplash', 'mixed'] and not unsplash_limit_hit:
            new_image = self.search_unsplash(keywords)
            if new_image:
                if 'used_unsplash_ids' not in self.history:
                    self.history['used_unsplash_ids'] = []
                self.history['used_unsplash_ids'].append(new_image['id'])
        
        force_fallback = (strategy == 'unsplash' and unsplash_limit_hit)
        
        if not new_image and (strategy in ['volcengine', 'mixed'] or force_fallback):
            if unsplash_limit_hit and strategy == 'unsplash':
                 print(f"Forcing Volcengine fallback due to Unsplash limit ({self.unsplash_limit})")
            new_image = self.generate_volcengine(keywords)

        if new_image:
            if dry_run:
                print(f"[DRY RUN] Would replace image in {filepath} with: {new_image['url']}")
            else:
                if self.config.get('backup', True):
                    shutil.copy(filepath, f"{filepath}.bak")
                
                # Matches: https://images.unsplash.com/photo-ID... optionally followed by query params
                # Also matches: https://source.unsplash.com/...
                
                # 1. Replace standard Unsplash ID
                pattern_id = r'https://images\.unsplash\.com/' + re.escape(DEFAULT_IMAGE) + r'(\?[^\s\)\"\']*)?'
                content = re.sub(pattern_id, new_image['url'], content)
                
                # 2. Replace source.unsplash.com (legacy broken links)
                pattern_source = r'https://source\.unsplash\.com/[^\s\)\"\']+'
                content = re.sub(pattern_source, new_image['url'], content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Updated {filepath}")
                self.save_history()
        else:
            print(f"Skipping {filepath}: Could not find/generate replacement image.")

    def run(self, dry_run=False):
        files = glob.glob(f"{BLOG_DIR}/**/*.md", recursive=True)
        print(f"Scanning {len(files)} files for duplicate images...")
        count = 0
        for filepath in files:
            # Check if file needs processing (contains default image OR broken source link)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                needs_update = (DEFAULT_IMAGE in content) or ('source.unsplash.com' in content)
                
                if needs_update:
                    self.process_file(filepath, dry_run)
                    count += 1
            except Exception as e:
                print(f"Error checking {filepath}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Smart Image Replacer')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes')
    args = parser.parse_args()

    manager = ImageManager()
    manager.run(dry_run=args.dry_run)

if __name__ == '__main__':
    main()
