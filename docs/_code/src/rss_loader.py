import feedparser
import requests
from typing import List, Dict
from datetime import datetime
import config


def load_rss_entries() -> List[Dict]:
    entries = []
    
    if not config.ENABLE_RSS:
        return entries
    
    for source in config.RSS_SOURCES:
        try:
            feed = feedparser.parse(source['url'])
            
            for entry in feed.entries[:20]:
                title = entry.get('title', '')
                link = entry.get('link', '')
                summary = entry.get('summary', '')[:500]
                published = entry.get('published', '')
                
                keywords = source.get('keywords', [])
                title_lower = title.lower()
                
                if keywords and not any(k.lower() in title_lower for k in keywords):
                    continue
                
                entries.append({
                    'source_type': 'rss',
                    'source_name': source['name'],
                    'title': title,
                    'url': link,
                    'summary': summary,
                    'published': published,
                    'keywords': keywords,
                    'lang': 'en'
                })
        except Exception as e:
            print(f"  RSS加载失败 [{source['name']}]: {e}")
    
    return entries


def fetch_rss_content(url: str) -> str:
    try:
        response = requests.get(url, timeout=config.SPIDER_TIMEOUT)
        response.raise_for_status()
        return response.text[:5000]
    except Exception as e:
        return f"Error fetching: {e}"
