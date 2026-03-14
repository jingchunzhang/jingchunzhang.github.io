import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin
import concurrent.futures
import config


def fetch_page(url: str) -> str:
    try:
        response = requests.get(url, timeout=config.SPIDER_TIMEOUT)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return ""


def parse_article(html: str, selectors: Dict) -> Dict:
    soup = BeautifulSoup(html, 'html.parser')
    
    article_elem = soup.select_one(selectors.get('article', 'article'))
    if not article_elem:
        return {}
    
    title = ""
    title_sel = selectors.get('title', 'h1')
    title_elem = article_elem.select_one(title_sel)
    if not title_elem:
        title_elem = soup.select_one(title_sel)
    if title_elem:
        title = title_elem.get_text(strip=True)
    
    content = ""
    content_sel = selectors.get('content', 'div')
    content_elem = article_elem.select_one(content_sel)
    if not content_elem:
        content_elem = soup.select_one(content_sel)
    if content_elem:
        content = content_elem.get_text(strip=True)[:2000]
    
    links = []
    link_sel = selectors.get('link', 'a')
    for link in article_elem.select(link_sel)[:10]:
        href = link.get('href', '')
        if href:
            links.append(href)
    
    return {
        'title': title,
        'content': content,
        'links': links
    }


def crawl_source(source: Dict) -> List[Dict]:
    articles = []
    base_url = source['url']
    keywords = source.get('keywords', [])
    selectors = source.get('selectors', {})
    
    html = fetch_page(base_url)
    if not html:
        return articles
    
    soup = BeautifulSoup(html, 'html.parser')
    
    link_selector = selectors.get('link', 'a')
    article_links = soup.select(link_selector)
    
    matching_links = []
    for link in article_links:
        href = link.get('href', '')
        if not href:
            continue
        
        full_url = urljoin(base_url, href)
        
        if any(k.lower() in full_url.lower() for k in keywords):
            matching_links.append(full_url)
    
    for full_url in matching_links[:10]:
            article_html = fetch_page(full_url)
            if article_html:
                article_data = parse_article(article_html, selectors)
                if article_data.get('title'):
                    articles.append({
                        'source_type': 'spider',
                        'source_name': source['name'],
                        'title': article_data['title'],
                        'url': full_url,
                        'content': article_data['content'],
                        'keywords': keywords,
                        'lang': 'en'
                    })
    
    return articles


def load_spider_entries() -> List[Dict]:
    entries = []
    
    if not config.ENABLE_SPIDER:
        return entries
    
    print(f"  爬虫数据源: {len(config.SPIDER_SOURCES)} 个")
    
    for source in config.SPIDER_SOURCES:
        try:
            print(f"    正在抓取: {source['name']}")
            articles = crawl_source(source)
            entries.extend(articles)
            print(f"      获取 {len(articles)} 篇文章")
        except Exception as e:
            print(f"      抓取失败: {e}")
    
    return entries
