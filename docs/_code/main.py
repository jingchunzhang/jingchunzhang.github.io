"""
Blog Content Automation System
每日任务入口
"""

import sys
from pathlib import Path
from datetime import datetime
import re
import config

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.ebook_loader import get_pending_topics
from src.data_source_loader import load_all_sources
from src.vector_store import VectorStore
from src.content_generator import ContentGenerator, generate_front_matter, parse_llm_output
from src.publisher import Publisher
from src.index_updater import add_new_post_links
from src.content_classifier import classify_content, get_subdir

def sanitize_slug(text: str) -> str:
    """Sanitize slug to be English + Date + Hyphens only"""
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    text = text.strip().lower().replace(' ', '-')
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text[:50]

def run_daily_task():
    print("=" * 50)
    print(f"开始每日任务: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    print("\n[1/6] 加载数据源...")
    all_topics = load_all_sources()
    print(f"  - 加载了 {len(all_topics)} 条选题")
    
    print("\n[2/6] 获取已存在文章...")
    publisher = Publisher()
    existing_slugs = publisher.get_existing_slugs()
    print(f"  - 已有 {len(existing_slugs)} 篇文章")
    
    print("\n[3/6] 获取待生成选题...")
    pending_topics = []
    for topic in all_topics:
        slug = topic.get('slug', '')
        source = topic.get('source', '')
        
        if source == 'ebook':
            if slug and slug not in existing_slugs:
                pending_topics.append(topic)
        elif source in ['rss', 'spider']:
            keyword = topic.get('keyword', '')
            if keyword:
                temp_slug = sanitize_slug(keyword)
                if temp_slug and temp_slug not in existing_slugs:
                    pending_topics.append(topic)
    
    print(f"  - 待生成 {len(pending_topics)} 篇")
    
    if not pending_topics:
        print("\n没有待生成的选题，任务结束")
        return
    
    topics_to_generate = pending_topics[:config.DAILY_POST_LIMIT]
    print(f"  - 本次将生成 {len(topics_to_generate)} 篇 (中英文各一篇)")
    
    print("\n[4/6] 初始化服务...")
    vector_store = VectorStore()
    generator = ContentGenerator()
    
    print("\n[5/6] 生成文章...")
    generated_count = 0
    generated_posts = []
    
    used_images = set()
    
    for i, topic in enumerate(topics_to_generate):
        keyword = topic.get('keyword', '')
        print(f"\n  [{i+1}/{len(topics_to_generate)}] 处理: {keyword[:40]}...")
        
        similarity = vector_store.check_similarity(keyword)
        
        if similarity > config.SIMILARITY_THRESHOLD:
            print(f"    - 跳过: 相似度 {similarity:.2f} 超过阈值")
            continue
        
        try:
            date_str = datetime.now().strftime('%Y-%m-%d')
            
            print(f"    - 生成英文内容...")
            content_en = generator.generate_with_retry(keyword, lang="en")
            
            content_en = generator.inject_image(content_en, used_images, keyword=keyword)
            
            parsed_en = parse_llm_output(content_en)
            title_en = parsed_en.get('title', '') or keyword
            print(f"    - Using title (EN): {title_en}")
            
            base_slug = sanitize_slug(title_en)
            if not base_slug or len(base_slug) < 3:
                 base_slug = sanitize_slug(keyword)
            
            if not base_slug:
                 print(f"    - 错误: 无法生成有效 Slug, 跳过")
                 continue
                 
            slug_zh = f"{date_str}-{base_slug}"
            slug_en = f"{slug_zh}-en"
            print(f"    - Slug: {slug_zh}")
            
            if slug_zh in existing_slugs:
                 print(f"    - 跳过: Slug 已存在 ({slug_zh})")
                 continue

            print(f"    - 生成中文内容...")
            content_zh = generator.generate_with_retry(keyword, lang="zh")
            content_zh = generator.inject_image(content_zh, used_images, keyword=keyword)
            
            parsed_zh = parse_llm_output(content_zh)
            title_zh = parsed_zh.get('title', '') or keyword
            print(f"    - Using title (ZH): {title_zh}")
            
            topic['title_zh'] = title_zh
            topic['title_en'] = title_en
            topic['slug'] = slug_zh
            
            classification = classify_content(keyword, content_zh)
            subdir = get_subdir(classification['stage'], classification['aspect'])
            print(f"    - 分类: {classification['stage']}/{classification['aspect']}")
            
            publish_date = datetime.now()
            
            front_matter_zh = generate_front_matter(topic, publish_date, custom_title=title_zh)
            front_matter_en = generate_front_matter(topic, publish_date, custom_title=title_en)
            
            publisher.create_blog_post(slug_zh, content_zh, front_matter_zh, subdir=subdir)
            publisher.create_blog_post(slug_en, content_en, front_matter_en, subdir=subdir)
            
            generated_count += 2
            
            generated_posts.append({
                'slug': slug_zh,
                'title_zh': title_zh,
                'title_en': title_en,
                'subdir': subdir
            })
            
            vector_store.add_documents(
                ids=[slug_zh, slug_en],
                documents=[content_zh, content_en],
                metadatas=[
                    {'keyword': keyword, 'slug': slug_zh, 'date': publish_date.isoformat(), 'lang': 'zh'},
                    {'keyword': keyword, 'slug': slug_en, 'date': publish_date.isoformat(), 'lang': 'en'}
                ]
            )
            
            print(f"    - 已生成: {slug_zh} (中文) + {slug_en} (英文)")
            
        except Exception as e:
            print(f"    - 生成失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n[5.5/6] 更新索引...")
    if generated_posts:
        add_new_post_links(generated_posts)
        print(f"  - 已更新 index.md 和 index-en.md")
    
    print("\n[6/6] Git提交推送...")
    if generated_count > 0:
        publisher.git_add_commit_push(f"Auto publish {generated_count} posts - {datetime.now().strftime('%Y-%m-%d')}")
    else:
        print("  - 没有新内容需要推送")
    
    print("\n" + "=" * 50)
    print(f"任务完成: 生成了 {generated_count} 篇文章")
    print("=" * 50)


if __name__ == "__main__":
    run_daily_task()
