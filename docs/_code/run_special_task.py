import sys
from pathlib import Path
from datetime import datetime
import random
import time

sys.path.insert(0, str(Path(__file__).parent))

import config
from src.longtail_manager import generate_dimensional_keywords
from src.content_generator import ContentGenerator, generate_front_matter, parse_llm_output
from src.publisher import Publisher
from src.index_updater import add_new_post_links
from src.content_classifier import classify_content, get_subdir
from src.vector_store import VectorStore

def run_special_task():
    print("=" * 50)
    print(f"Start Special Task: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. Generate Dimensional Keywords
    base_keywords = config.EBOOK_KEYWORDS
    print(f"Base keywords: {base_keywords}")
    
    dimensional_keywords = generate_dimensional_keywords(base_keywords)
    print(f"Generated {len(dimensional_keywords)} dimensional keywords.")
    
    # 2. Select 3-4 keywords
    selected_keywords = random.sample(dimensional_keywords, 4)
    print(f"Selected keywords: {selected_keywords}")
    
    # We need to generate 5 posts. So we'll use the first keyword twice? 
    # Or just select 5 keywords? Let's select 5 keywords to be simple.
    # The prompt says "pick 3-4 long-tail keywords, write 5 blogs".
    # So I will select 3 keywords, and for the first two, I'll generate 2 variants (maybe different personas?), 
    # and for the last one, 1 variant.
    
    topics_to_generate = []
    
    # Keyword 1 -> 2 posts
    topics_to_generate.append({'keyword': selected_keywords[0], 'variant': 'A'})
    topics_to_generate.append({'keyword': selected_keywords[0], 'variant': 'B'})
    
    # Keyword 2 -> 2 posts
    topics_to_generate.append({'keyword': selected_keywords[1], 'variant': 'A'})
    topics_to_generate.append({'keyword': selected_keywords[1], 'variant': 'B'})
    
    # Keyword 3 -> 1 post
    topics_to_generate.append({'keyword': selected_keywords[2], 'variant': 'A'})
    
    print(f"Plan to generate {len(topics_to_generate)} posts.")
    
    # 3. Generate Content
    generator = ContentGenerator()
    publisher = Publisher()
    vector_store = VectorStore()
    
    generated_posts = []
    
    for i, topic in enumerate(topics_to_generate):
        keyword = topic['keyword']
        variant = topic['variant']
        print(f"\nProcessing [{i+1}/{len(topics_to_generate)}]: {keyword} (Variant {variant})")
        
        try:
            date_str = datetime.now().strftime('%Y-%m-%d')
            
            # Chinese
            print("  Generating ZH...")
            content_zh = generator.generate_with_retry(keyword, lang="zh")
            parsed_zh = parse_llm_output(content_zh)
            title_zh = parsed_zh.get('title', '') or keyword
            
            slug_base = keyword.lower().replace(' ', '-')[:40]
            # Add variant to slug to avoid collision
            slug_zh = f"{date_str}-{slug_base}-{variant.lower()}"
            
            # English
            print("  Generating EN...")
            content_en = generator.generate_with_retry(keyword, lang="en")
            parsed_en = parse_llm_output(content_en)
            title_en = parsed_en.get('title', '') or keyword
            
            slug_en = f"{slug_zh}-en"
            
            # Classification & Subdir
            classification = classify_content(keyword, content_zh)
            subdir = get_subdir(classification['stage'], classification['aspect'])
            
            publish_date = datetime.now()
            
            # Front Matter
            topic_data = {
                'keyword': keyword,
                'slug': slug_zh,
                'disclaimer_key': 'medical-information-only'
            }
            
            fm_zh = generate_front_matter(topic_data, publish_date, custom_title=title_zh)
            fm_en = generate_front_matter(topic_data, publish_date, custom_title=title_en)
            
            # Save
            publisher.create_blog_post(slug_zh, content_zh, fm_zh, subdir=subdir)
            publisher.create_blog_post(slug_en, content_en, fm_en, subdir=subdir)
            
            generated_posts.append({
                'slug': slug_zh,
                'title_zh': title_zh,
                'title_en': title_en,
                'subdir': subdir
            })
            
            # Vector Store Update
            vector_store.add_documents(
                ids=[slug_zh, slug_en],
                documents=[content_zh, content_en],
                metadatas=[
                    {'keyword': keyword, 'slug': slug_zh, 'date': publish_date.isoformat(), 'lang': 'zh'},
                    {'keyword': keyword, 'slug': slug_en, 'date': publish_date.isoformat(), 'lang': 'en'}
                ]
            )
            
            print(f"  Saved: {slug_zh} & {slug_en}")
            
            # Sleep briefly to avoid rate limits if any
            time.sleep(2)
            
        except Exception as e:
            print(f"  Failed: {e}")
            import traceback
            traceback.print_exc()

    # 4. Update Index & Git Push
    if generated_posts:
        print("\nUpdating index...")
        add_new_post_links(generated_posts)
        
        print("\nPushing to Git...")
        publisher.git_add_commit_push(f"Auto publish {len(generated_posts)} posts (Special Task) - {datetime.now().strftime('%Y-%m-%d')}")
        
    print("\nTask Complete.")

if __name__ == "__main__":
    run_special_task()
