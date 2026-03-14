import csv
from pathlib import Path
from typing import List, Dict
import config

def load_manifest(manifest_file: str = None) -> List[Dict]:
    """加载 ebook manifest CSV"""
    if manifest_file:
        manifest_path = Path(manifest_file)
    else:
        # 加载最新的 manifest
        manifests = sorted(config.EBOOK_MANIFEST_DIR.glob("*.csv"))
        if not manifests:
            return []
        manifest_path = manifests[-1]
    
    results = []
    with open(manifest_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('status') == 'ready':
                results.append(row)
    return results

def load_author_rotation() -> List[Dict]:
    """加载作者轮换表"""
    results = []
    with open(config.EBOOK_AUTHOR_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    return results

def get_author_for_date(publish_date) -> Dict:
    """根据发布日期获取作者信息"""
    import datetime
    authors = load_author_rotation()
    if not authors:
        return {"author_id": "default", "author_role": "AI Writer"}
    
    # 计算星期几 (周一=1, 周日=7)
    weekday = publish_date.weekday() + 1
    index = weekday % len(authors)
    return authors[index]

def extract_search_intents(manifests: List[Dict]) -> List[Dict]:
    """从 manifest 中提取搜索意图列表"""
    intents = []
    for m in manifests:
        # 中文搜索意图
        if m.get('target_search_intent'):
            intents.append({
                'keyword': m['target_search_intent'],
                'lang': 'zh',
                'slug': m.get('target_blog_slug', ''),
                'path': m.get('target_blog_path', ''),
                'download_url': m.get('public_url', ''),
                'source': 'ebook_manifest'
            })
        # 英文搜索意图
        if m.get('target_search_intent'):
            # 需要区分中英文，可能需要通过 slug 判断
            pass
    return intents

def get_pending_topics(manifests: List[Dict], existing_slugs: List[str]) -> List[Dict]:
    """获取尚未创建文章的选题"""
    pending = []
    for m in manifests:
        slug = m.get('target_blog_slug', '')
        if slug and slug not in existing_slugs and m.get('status') == 'ready':
            pending.append({
                'keyword': m.get('target_search_intent', ''),
                'slug': slug,
                'path': m.get('target_blog_path', ''),
                'download_url': m.get('public_url', ''),
                'author_id': m.get('author_id', ''),
                'author_email': m.get('author_email', ''),
                'author_role': m.get('author_role', ''),
                'disclaimer_key': m.get('disclaimer_key', 'medical-information-only')
            })
    return pending
