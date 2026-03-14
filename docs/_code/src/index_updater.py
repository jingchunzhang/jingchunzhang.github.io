from pathlib import Path
import re
from datetime import datetime
import config

def get_index_files():
    blog_dir = config.BLOG_SOURCE_DIR
    zh_index = blog_dir / "index.md"
    en_index = blog_dir / "index-en.md"
    return zh_index, en_index

def add_link_to_index(slug: str, title: str, lang: str = "zh"):
    """添加博客链接到index文件"""
    zh_index, en_index = get_index_files()
    
    if lang == "zh":
        _add_link(zh_index, slug, title)
    else:
        _add_link(en_index, slug, title)

def _add_link(index_file: Path, slug: str, title: str):
    if not index_file.exists():
        return
    
    content = index_file.read_text(encoding='utf-8')
    
    link_markdown = f"*   **[{title}](./{slug})**"
    
    if link_markdown in content:
        return
    
    lines = content.split('\n')
    
    insert_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('## ') and ('最新' in line or 'Latest' in line):
            insert_idx = i + 1
            break
    
    if insert_idx is None:
        for i, line in enumerate(lines):
            if line.strip().startswith('*   **['):
                insert_idx = i
                break
    
    if insert_idx is not None:
        lines.insert(insert_idx, link_markdown)
        content = '\n'.join(lines)
        index_file.write_text(content, encoding='utf-8')

def add_links_batch(posts: list):
    """批量添加链接到index文件"""
    zh_index, en_index = get_index_files()
    
    new_zh_links = []
    new_en_links = []
    
    for post in posts:
        slug = post.get('slug', '')
        title_zh = post.get('title_zh', '')
        title_en = post.get('title_en', '')
        
        if title_zh:
            new_zh_links.append(f"*   **[{title_zh}](./{slug})**")
        if title_en:
            new_en_links.append(f"*   **[{title_en}](./{slug}-en)**")
    
    if new_zh_links:
        _batch_add_links(zh_index, new_zh_links)
    if new_en_links:
        _batch_add_links(en_index, new_en_links)

def _batch_add_links(index_file: Path, new_links: list):
    if not index_file.exists():
        return
    
    content = index_file.read_text(encoding='utf-8')
    
    for link in new_links:
        if link in content:
            new_links.remove(link)
    
    if not new_links:
        return
    
    lines = content.split('\n')
    
    insert_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('## '):
            insert_idx = i + 1
            break
    
    if insert_idx is None:
        insert_idx = 10
    
    for link in reversed(new_links):
        lines.insert(insert_idx, link)
    
    content = '\n'.join(lines)
    index_file.write_text(content, encoding='utf-8')
