import csv
from pathlib import Path
from typing import List, Dict
import config


def load_all_sources() -> List[Dict]:
    """加载所有数据源的选题"""
    all_topics = []
    
    if config.ENABLE_EBOOK:
        print("  [Ebook] 加载中...")
        ebook_topics = load_manifest()
        for topic in ebook_topics:
            topic['source'] = 'ebook'
            topic['keyword'] = topic.get('target_search_intent', '')
            topic['slug'] = topic.get('target_blog_slug', '')
            topic['path'] = topic.get('target_blog_path', '')
            topic['download_url'] = topic.get('public_url', '')
            topic['lang'] = 'zh' if '糖尿病' in topic.get('target_search_intent', '') else 'en'
        all_topics.extend(ebook_topics)
        print(f"    - 获取 {len(ebook_topics)} 条选题")
    
    if config.ENABLE_RSS:
        print("  [RSS] 加载中...")
        try:
            from src.rss_loader import load_rss_entries
            rss_entries = load_rss_entries()
            for entry in rss_entries:
                entry['source'] = 'rss'
                entry['keyword'] = entry.get('title', '')[:100]
            all_topics.extend(rss_entries)
            print(f"    - 获取 {len(rss_entries)} 条选题")
            
            from src.longtail_manager import extract_longtail_keywords
            new_keywords = extract_longtail_keywords(rss_entries)
            if new_keywords:
                from src.longtail_manager import LongTailManager
                ltm = LongTailManager()
                ltm.add_pending(new_keywords)
                print(f"    - 添加 {len(new_keywords)} 个长尾词到待处理")
        except Exception as e:
            print(f"    - RSS加载失败: {e}")
    
    if config.ENABLE_SPIDER:
        print("  [Spider] 加载中...")
        try:
            from src.spider_loader import load_spider_entries
            spider_entries = load_spider_entries()
            for entry in spider_entries:
                entry['source'] = 'spider'
                entry['keyword'] = entry.get('title', '')[:100]
            all_topics.extend(spider_entries)
            print(f"    - 获取 {len(spider_entries)} 条选题")
            
            from src.longtail_manager import extract_longtail_keywords
            new_keywords = extract_longtail_keywords(spider_entries)
            if new_keywords:
                from src.longtail_manager import LongTailManager
                ltm = LongTailManager()
                ltm.add_pending(new_keywords)
                print(f"    - 添加 {len(new_keywords)} 个长尾词到待处理")
        except Exception as e:
            print(f"    - 爬虫加载失败: {e}")
    
    print(f"  总计: {len(all_topics)} 条选题")
    return all_topics


def load_manifest(manifest_file: str = None) -> List[Dict]:
    """加载 ebook manifest CSV - 使用csv模块处理"""
    if manifest_file:
        manifest_path = Path(manifest_file)
    else:
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
    
    weekday = publish_date.weekday() + 1
    index = weekday % len(authors)
    return authors[index]


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
