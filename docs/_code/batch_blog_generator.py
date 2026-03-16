import json
import requests
import sys
from datetime import datetime
from pathlib import Path
import random

CONFIG = {
    'api_base': 'https://ark.cn-beijing.volces.com/api/v3',
    'api_key': '54bf396f-61d1-4ef9-95d2-1da543cbd838',
    'model': 'doubao-seed-1-6-flash-250828',
}

AUTHOR_INFO = {
    'zzh': {
        'author_id': 'zzh',
        'author_name': 'zzh',
        'author_email': 'zzh@tangyou.space',
        'author_role': '糖尿病治疗期病人',
        'reviewer_id': 'yyh',
        'reviewer_name': 'yyh',
        'reviewer_email': 'yyh@tangyou.space',
        'reviewer_role': '糖尿病治疗医生'
    }
}

GENRE_VARIANTS = {
    "对比清单": """请生成一篇"{keyword}"的对比清单文章。要求：
1. 列出 3-5 个关键对比点
2. 每个对比点用表格或列表清晰展示
3. 给出明确的优缺点总结
4. 适合糖尿病患者或高危人群阅读""",
    
    "step_by_step": """请生成一篇"{keyword}"的 Step-by-step 教程。要求：
1. 使用清晰的步骤编号
2. 每个步骤包含具体操作说明
3. 添加"小贴士"或"注意事项"
4. 语言通俗易懂，适合新手""",
    
    "avoidance_guide": """请生成一篇"{keyword}"的避坑指南。要求：
1. 列出常见的 5-8 个误区或错误做法
2. 解释为什么这些是错的
3. 提供正确的做法或替代方案
4. 语气友善，像朋友提醒""",
    
    "experience_share": """请生成一篇"{keyword}"的经验分享文章。要求：
1. 第一人称叙述，有真实感
2. 分享具体的使用体验或经历
3. 包含成功经验和踩坑经历
4. 情感真挚，避免过于机械"""
}

YMYL_DISCLAIMER = "本文由AI辅助生成，仅供信息参考，不构成医疗建议。请咨询专业医生后再做决策。"

def generate_content(prompt: str) -> str:
    url = f"{CONFIG['api_base']}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CONFIG['api_key']}"
    }
    data = {
        "model": CONFIG['model'],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=120)
    response.raise_for_status()
    result = response.json()
    
    return result['choices'][0]['message']['content']


def build_zh_prompt(keyword: str, genre: str = None) -> str:
    if genre is None:
        genre = random.choice(list(GENRE_VARIANTS.keys()))
    
    genre_template = GENRE_VARIANTS.get(genre, GENRE_VARIANTS["step_by_step"])
    
    prompt = f"""你是一位有着 10 年糖尿病管理经验的资深糖友，亲身尝试过各种方法。
写作风格：温暖、耐心、经验丰富，分享的经历让人感到可信和安心。

请用简体中文写作。

{genre_template}

{YMYL_DISCLAIMER}

请生成一篇高质量的文章，围绕关键词：{keyword}

文章要求：
- 字数 1500-2000 字
- 结构清晰，有明确的小标题（H2, H3）
- 适合 SEO，包含关键词的自然分布
- 在文章开头或适当位置添加1-2张相关图片（使用 Markdown 图片语法，描述性 alt 文本）
- 结尾引导下载相关电子书
- 包含 FAQ 部分

请生成完整的Markdown文章内容。"""
    return prompt


def build_en_prompt(keyword: str, genre: str = None) -> str:
    if genre is None:
        genre = random.choice(list(GENRE_VARIANTS.keys()))
    
    genre_template = GENRE_VARIANTS.get(genre, GENRE_VARIANTS["step_by_step"])
    
    prompt = f"""You are a资深糖尿病患者 with 10 years of experience managing diabetes, having tried various methods personally.
Writing style: warm, patient, experienced, sharing experiences that make people feel credible and at ease.

Please write in English.

{genre_template}

This article is for informational purposes only and does not constitute medical advice. Please consult your doctor before making any health decisions.

Please generate a high-quality article around the keyword: {keyword}

Article requirements:
- 1200-1800 words
- Clear structure with H2, H3 headings
- SEO-friendly, natural keyword distribution
- Add 1-2 relevant images using Markdown image syntax with descriptive alt text
- Include an ebook download CTA at the end
- Include an FAQ section

Please generate the complete Markdown article content."""
    return prompt


def generate_blog(keyword: str, is_english: bool = False, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        try:
            if is_english:
                prompt = build_en_prompt(keyword)
            else:
                prompt = build_zh_prompt(keyword)
            
            content = generate_content(prompt)
            return content
        except Exception as e:
            print(f"生成失败 (尝试 {attempt + 1}/{max_retries}): {e}")
    
    raise Exception(f"内容生成失败，已重试 {max_retries} 次")


def create_front_matter(blog: dict, author_info: dict) -> str:
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    if blog['is_english']:
        title = blog['keyword'].title()
        description = f"{blog['keyword']} - Comprehensive guide for diabetes prevention"
    else:
        title = blog['keyword']
        description = f"{blog['keyword']} - 糖尿病预防全面指南"
    
    fm = f"""---
title: "{title}"
date: {date_str}
lang: {"en" if blog['is_english'] else "zh"}
translation_key: {blog['slug'].replace('-en', '')}
description: "{description}"
categories: ["{blog['stage']}", "{blog['dimension']}"]
tags: ["糖尿病预防", "备餐", "健康饮食"]
author_id: "{author_info['author_id']}"
author_name: "{author_info['author_name']}"
author_email: "{author_info['author_email']}"
author_role: "{author_info['author_role']}"
reviewer_id: "{author_info['reviewer_id']}"
reviewer_name: "{author_info['reviewer_name']}"
reviewer_email: "{author_info['reviewer_email']}"
reviewer_role: "{author_info['reviewer_role']}"
review_status: "draft"
disclaimer_key: "medical-information-only"
download_url: "https://download.tangyou.space/20260311/Diabetic-Meal-Prep-for-Beginners-Cookbook-with-30-Day-Meal-Plan-to-Prevent-and-Reverse-Diabetes-Simple-and-Healthy-Recipes.epub"
slug: "{blog['slug']}"
---

"""
    return fm


def save_blog(blog: dict, content: str, author_info: dict):
    stage = blog['stage']
    dimension = blog['dimension']
    slug = blog['slug']
    
    blog_dir = Path(f"blog/{stage}/{dimension}")
    blog_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = blog_dir / f"{slug}.md"
    
    front_matter = create_front_matter(blog, author_info)
    full_content = front_matter + content
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"已保存: {file_path}")
    return file_path


def main():
    with open('_code/temp/blog_tasks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    blogs = data['blogs']
    author_info = data['author_info']
    
    print(f"开始生成 {len(blogs)} 篇博客...")
    print(f"作者: {author_info['author_id']} ({author_info['author_role']})")
    print("-" * 50)
    
    zh_blogs = [b for b in blogs if not b['is_english']]
    en_blogs = [b for b in blogs if b['is_english']]
    
    print(f"中文博客: {len(zh_blogs)} 篇")
    print(f"英文博客: {len(en_blogs)} 篇")
    
    print("\n>>> 开始生成中文博客 <<<")
    for i, blog in enumerate(zh_blogs, 1):
        print(f"[{i}/{len(zh_blogs)}] 生成: {blog['keyword']}")
        try:
            content = generate_blog(blog['keyword'], is_english=False)
            save_blog(blog, content, author_info)
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n>>> 开始生成英文博客 <<<")
    for i, blog in enumerate(en_blogs, 1):
        print(f"[{i}/{len(en_blogs)}] 生成: {blog['keyword']}")
        try:
            content = generate_blog(blog['keyword'], is_english=True)
            save_blog(blog, content, author_info)
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n" + "=" * 50)
    print("博客生成完成!")


if __name__ == '__main__':
    main()
