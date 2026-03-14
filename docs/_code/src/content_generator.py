import os
import google.generativeai as genai
from typing import Dict, Optional
import config
from src.prompt_pool import build_prompt, get_random_variant

class ContentGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(config.GEMINI_MODEL)
    
    def generate(self, keyword: str, genre: str = None, persona: str = None) -> str:
        """生成文章内容"""
        if not self.api_key:
            raise Exception("未配置 GEMINI_API_KEY")
        
        prompt = build_prompt(keyword, genre, persona)
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_with_retry(self, keyword: str, max_retries: int = 3) -> str:
        """带重试的内容生成"""
        for attempt in range(max_retries):
            try:
                genre, persona = get_random_variant()
                content = self.generate(keyword, genre, persona)
                
                # 安全检查
                if self._safe_check(content):
                    return content
                else:
                    print(f"内容安全检查未通过，重试 {attempt + 1}/{max_retries}")
                    
            except Exception as e:
                print(f"生成失败: {e}, 重试 {attempt + 1}/{max_retries}")
        
        raise Exception(f"内容生成失败，已重试 {max_retries} 次")
    
    def _safe_check(self, content: str) -> bool:
        """YMYL 领域安全检查"""
        for blocked in config.BLOCKED_KEYWORDS:
            if blocked in content:
                print(f"警告: 内容包含敏感词: {blocked}")
                return False
        return True

def generate_front_matter(topic: Dict, publish_date) -> str:
    """生成 Jekyll Front Matter"""
    from src.ebook_loader import get_author_for_date
    
    author_info = get_author_for_date(publish_date)
    
    date_str = publish_date.strftime("%Y-%m-%d %H:%M:%S +0800")
    
    fm = f"""---
title: "{topic.get('keyword', '')}"
date: {date_str}
description: "{topic.get('keyword', '')} - 糖尿病知识全面解读"
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
    
    # 简单处理：假设输出直接是正文
    # 后续可以加入 markdown 解析
    
    return {
        'content': raw_output,
        'title': '',  # 可以用 LLM 生成标题，或从关键词提取
        'excerpt': raw_output[:200] + '...'
    }
