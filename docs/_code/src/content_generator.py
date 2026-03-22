import os
import requests
from typing import Dict, Optional
import config
from src.prompt_pool import build_prompt, get_random_variant


class ContentGenerator:
    def __init__(self, api_key: str = None):
        self.use_volcengine = config.USE_VOLCENGINE_LLM
        self.volcengine_api_key = config.VOLCENGINE_LLM_API_KEY
        self.volcengine_model = config.VOLCENGINE_LLM_MODEL
        self.volcengine_api_base = config.VOLCENGINE_LLM_API_BASE
        
        self.gemini_api_key = api_key or config.GEMINI_API_KEY
        self.gemini_model = config.GEMINI_MODEL
        
        if not self.use_volcengine and not self.gemini_api_key:
            self._api_available = False
        else:
            self._api_available = True
    
    def generate(self, keyword: str, genre: str = None, persona: str = None, lang: str = "zh") -> str:
        if not self._api_available:
            raise Exception("未配置任何LLM API (GEMINI_API_KEY 或 VOLCENGINE_LLM_API_KEY)")
        
        prompt = build_prompt(keyword, genre, persona, lang)
        
        if self.use_volcengine and self.volcengine_api_key:
            return self._generate_volcengine(prompt)
        else:
            return self._generate_gemini(prompt)
    
    def _generate_volcengine(self, prompt: str) -> str:
        url = f"{self.volcengine_api_base}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.volcengine_api_key}"
        }
        data = {
            "model": self.volcengine_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        result = response.json()
        
        return result['choices'][0]['message']['content']
    
    def _generate_gemini(self, prompt: str) -> str:
        import google.generativeai as genai
        genai.configure(api_key=self.gemini_api_key)
        model = genai.GenerativeModel(self.gemini_model)
        response = model.generate_content(prompt)
        return response.text
    
    def generate_with_retry(self, keyword: str, max_retries: int = 3, lang: str = "zh") -> str:
        for attempt in range(max_retries):
            try:
                genre, persona = get_random_variant()
                content = self.generate(keyword, genre, persona, lang)
                
                if self._safe_check(content):
                    return content
                else:
                    print(f"内容安全检查未通过，重试 {attempt + 1}/{max_retries}")
                    
            except Exception as e:
                print(f"生成失败: {e}, 重试 {attempt + 1}/{max_retries}")
        
        raise Exception(f"内容生成失败，已重试 {max_retries} 次")
    
    def inject_image(self, content: str, used_images: set, keyword: str = "") -> str:
        """Replace image placeholder with unique image from pool"""
        from src.image_manager import image_manager
        import re
        
        pattern = image_manager.get_placeholder_pattern()
        
        matches = re.findall(pattern, content)

        def replace_match(match):
            alt_text = match.group(1)
            search_query = alt_text if len(alt_text) > 5 else keyword
            
            img_data = image_manager.get_image(search_query)
            
            if img_data:
                img_url = img_data['url']
                return f"![{alt_text}]({img_url})"
            else:
                return ""

        new_content = re.sub(pattern, replace_match, content)
        return new_content

    def _safe_check(self, content: str) -> bool:
        """YMYL 领域安全检查"""
        for blocked in config.BLOCKED_KEYWORDS:
            if blocked in content:
                print(f"警告: 内容包含敏感词: {blocked}")
                return False
        return True


def generate_front_matter(topic: Dict, publish_date, custom_title: Optional[str] = None) -> str:
     """生成 Jekyll Front Matter"""
     from src.ebook_loader import get_author_for_date
     
     author_info = get_author_for_date(publish_date)
     
     date_str = publish_date.strftime("%Y-%m-%dT%H:%M:%S+08:00")
     
     title = (custom_title or topic.get('keyword', '')).replace('"', '\\"')
     
     fm = f"""---
title: "{title}"
date: {date_str}
description: "{title} - 糖尿病知识全面解读"
categories: ["糖尿病预防"]
tags: ["糖尿病", "健康", "饮食"]
slug: {topic.get('slug', '')}

author_id: "{author_info.get('author_id', 'default')}"
author_email: "{author_info.get('author_email', '')}"
author_role: "{author_info.get('author_role', 'AI Writer')}"

review_status: "draft"
disclaimer_key: "{topic.get('disclaimer_key', 'medical-information-only')}"

download_url: "{topic.get('download_url', '')}"
---

"""
     return fm


def parse_llm_output(raw_output: str) -> Dict[str, str]:
     """解析 LLM 输出，分离正文和 Front Matter"""
     lines = raw_output.split('\n')
     
     title = ''
     for line in lines:
          stripped = line.strip()
          if stripped.startswith('# '):
               title = stripped[2:].strip()
               break
     
     return {
          'content': raw_output,
          'title': title,
          'excerpt': raw_output[:200] + '...'
     }
