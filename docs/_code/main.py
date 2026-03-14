"""
Blog Content Automation System
每日任务入口
"""

import sys
from pathlib import Path
from datetime import datetime
import config

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.ebook_loader import get_pending_topics
from src.data_source_loader import load_all_sources
from src.vector_store import VectorStore
from src.content_generator import ContentGenerator, generate_front_matter
from src.publisher import Publisher


def run_daily_task():
    """执行每日任务"""
    print("=" * 50)
    print(f"开始每日任务: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. 加载所有数据源
    print("\n[1/6] 加载数据源...")
    all_topics = load_all_sources()
    print(f"  - 加载了 {len(all_topics)} 条选题")
    
    # 2. 获取已存在的文章slug
    print("\n[2/6] 获取已存在文章...")
    publisher = Publisher()
    existing_slugs = publisher.get_existing_slugs()
    print(f"  - 已有 {len(existing_slugs)} 篇文章")
    
    # 3. 过滤待生成的选题
    print("\n[3/6] 获取待生成选题...")
    pending_topics = []
    for topic in all_topics:
        slug = topic.get('slug', '')
        source = topic.get('source', '')
        
        # 对于ebook，有预定slug
        if source == 'ebook':
            if slug and slug not in existing_slugs:
                pending_topics.append(topic)
        # 对于RSS和Spider，需要生成slug
        elif source in ['rss', 'spider']:
            keyword = topic.get('keyword', '')
            if keyword:
                # 生成slug
                slug = keyword.lower().replace(' ', '-')[:50]
                topic['slug'] = slug
                if slug not in existing_slugs:
                    pending_topics.append(topic)
    
    print(f"  - 待生成 {len(pending_topics)} 篇")
    
    if not pending_topics:
        print("\n没有待生成的选题，任务结束")
        return
    
    # 限制每日生成数量
    topics_to_generate = pending_topics[:config.DAILY_POST_LIMIT]
    print(f"  - 本次将生成 {len(topics_to_generate)} 篇")
    
    # 4. 初始化向量库和生成器
    print("\n[4/6] 初始化服务...")
    vector_store = VectorStore()
    generator = ContentGenerator()
    
    # 5. 生成并发布文章
    print("\n[5/6] 生成文章...")
    generated_count = 0
    
    for i, topic in enumerate(topics_to_generate):
        print(f"\n  [{i+1}/{len(topics_to_generate)}] 处理: {topic.get('keyword')}")
        
        # 向量库查重
        keyword = topic.get('keyword', '')
        similarity = vector_store.check_similarity(keyword)
        
        if similarity > config.SIMILARITY_THRESHOLD:
            print(f"    - 跳过: 相似度 {similarity:.2f} 超过阈值 {config.SIMILARITY_THRESHOLD}")
            continue
        
        # 生成内容
        try:
            content = generator.generate_with_retry(keyword)
            print(f"    - 生成成功")
        except Exception as e:
            print(f"    - 生成失败: {e}")
            continue
        
        # 生成Front Matter
        publish_date = datetime.now()
        front_matter = generate_front_matter(topic, publish_date)
        
        # 保存文章
        slug = topic.get('slug', '')
        try:
            publisher.create_blog_post(slug, content, front_matter)
            generated_count += 1
            
            # 添加到向量库
            vector_store.add_documents(
                ids=[slug],
                documents=[content],
                metadatas=[{
                    'keyword': keyword,
                    'slug': slug,
                    'date': publish_date.isoformat()
                }]
            )
            print(f"    - 保存成功")
            
        except Exception as e:
            print(f"    - 保存失败: {e}")
    
    # 6. Git提交推送
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
