from pathlib import Path
import re
from datetime import datetime, timedelta
import config

CATEGORY_NAMES = {
    ("prevention", "diet"): ("预防饮食", "Prevention Diet"),
    ("prevention", "exercise"): ("预防运动", "Prevention Exercise"),
    ("prevention", "sleep"): ("预防睡眠", "Prevention Sleep"),
    ("prevention", "emotion"): ("预防情绪", "Prevention Emotion"),
    ("treatment", "diet"): ("治疗饮食", "Treatment Diet"),
    ("treatment", "exercise"): ("治疗运动", "Treatment Exercise"),
    ("treatment", "sleep"): ("治疗睡眠", "Treatment Sleep"),
    ("treatment", "emotion"): ("治疗情绪", "Treatment Emotion"),
    ("rehabilitation", "diet"): ("康复饮食", "Rehabilitation Diet"),
    ("rehabilitation", "exercise"): ("康复运动", "Rehabilitation Exercise"),
    ("rehabilitation", "sleep"): ("康复睡眠", "Rehabilitation Sleep"),
    ("rehabilitation", "emotion"): ("康复情绪", "Rehabilitation Emotion"),
}

def get_index_files():
    blog_dir = config.BLOG_SOURCE_DIR
    zh_index = blog_dir / "index.md"
    en_index = blog_dir / "index-en.md"
    return zh_index, en_index

def add_links_batch(posts: list):
    for post in posts:
        subdir = post.get('subdir', '')
        if not subdir:
            continue
        
        slug = post.get('slug', '')
        title_zh = post.get('title_zh', '')
        title_en = post.get('title_en', '')
        
        parts = subdir.split('/')
        if len(parts) == 2:
            stage, aspect = parts
            
            subdir_index_zh = config.BLOG_SOURCE_DIR / subdir / "index.md"
            subdir_index_en = config.BLOG_SOURCE_DIR / subdir / "index-en.md"
            
            if title_zh:
                _add_link_to_subdir_index(subdir_index_zh, slug, title_zh)
            if title_en:
                _add_link_to_subdir_index(subdir_index_en, slug + "-en", title_en)

def _add_link_to_subdir_index(index_file: Path, slug: str, title: str):
    if not index_file.exists():
        return
    
    content = index_file.read_text(encoding='utf-8')
    
    link_markdown = f"### [{title}](./{slug}.md)"
    
    if link_markdown in content:
        return
    
    lines = content.split('\n')
    
    insert_idx = None
    for i, line in enumerate(lines):
        if "## " in line and "核心文章" in line:
            insert_idx = i + 1
            break
    
    if insert_idx is None:
        for i, line in enumerate(lines):
            if line.startswith('### ['):
                insert_idx = i
                break
    
    if insert_idx is not None:
        lines.insert(insert_idx, link_markdown)
        content = '\n'.join(lines)
        index_file.write_text(content, encoding='utf-8')

def update_new_posts(posts: list):
    zh_index, en_index = get_index_files()
    
    new_zh = []
    new_en = []
    
    for post in posts:
        slug = post.get('slug', '')
        title_zh = post.get('title_zh', '')
        title_en = post.get('title_en', '')
        subdir = post.get('subdir', '')
        
        if subdir:
            zh_link = f"*   **[{title_zh}](./{subdir}/{slug})**"
            en_link = f"*   **[{title_en}](./{subdir}/{slug}-en)**"
        else:
            zh_link = f"*   **[{title_zh}](./{slug})**"
            en_link = f"*   **[{title_en}](./{slug}-en)**"
        
        new_zh.append(zh_link)
        new_en.append(en_link)
    
    _update_new_section(zh_index, new_zh)
    _update_new_section(en_index, new_en)

def _update_new_section(index_file: Path, new_links: list):
    if not index_file.exists():
        return
    
    content = index_file.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    new_section_start = None
    new_section_end = None
    for i, line in enumerate(lines):
        if "最新更新" in line or "Latest" in line:
            new_section_start = i
            for j in range(i + 1, len(lines)):
                if lines[j].startswith('## '):
                    new_section_end = j
                    break
            if new_section_end is None:
                new_section_end = len(lines)
            break
    
    if new_section_start is None:
        return
    
    old_links = []
    for i in range(new_section_start + 1, new_section_end):
        if lines[i].startswith('*   **['):
            old_links.append(lines[i])
    
    all_links = new_links + old_links
    
    seen = set()
    unique_links = []
    for link in all_links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)
    
    all_links = unique_links[:10]
    
    lines = lines[:new_section_start + 1] + all_links + lines[new_section_end:]
    
    content = '\n'.join(lines)
    index_file.write_text(content, encoding='utf-8')

def add_new_post_links(posts: list):
    update_new_posts(posts)
    add_links_batch(posts)
