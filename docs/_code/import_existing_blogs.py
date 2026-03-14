"""
导入现有博客到Chroma向量库
扫描blog目录下所有.md文件，提取内容和metadata，批量导入到Chroma
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

import config
from src.vector_store import VectorStore


def parse_front_matter(content: str) -> tuple[dict, str]:
    """解析front matter，返回metadata和正文内容"""
    if not content.startswith('---'):
        return {}, content
    
    # 找到第二个 --- 的位置
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    front_matter_text = parts[1]
    body = parts[2].strip()
    
    # 解析 YAML 风格的 front matter
    metadata = {}
    for line in front_matter_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            metadata[key] = value
    
    return metadata, body


def extract_title_from_content(body: str) -> str:
    """从内容中提取标题"""
    # 尝试找第一个 # 标题
    match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    # 尝试找第一个 > 引用
    match = re.search(r'^>\s+(.+)$', body, re.MULTILINE)
    if match:
        return match.group(1).strip()[:100]
    
    # 取第一行作为标题
    lines = body.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line:
            return line[:100]
    
    return "untitled"


def get_all_blog_files(blog_dir: Path) -> list[Path]:
    """获取所有博客markdown文件，排除索引页和草稿"""
    blog_files = []
    
    # 排除的文件模式
    exclude_patterns = [
        'index.md',
        'index-en.md',
    ]
    
    for md_file in blog_dir.rglob('*.md'):
        # 跳过索引页
        if md_file.name in exclude_patterns:
            continue
        
        # 跳过草稿 (review_status: draft)
        try:
            content = md_file.read_text(encoding='utf-8')
            if 'review_status: draft' in content:
                print(f"  跳过草稿: {md_file.relative_to(blog_dir)}")
                continue
        except:
            pass
        
        blog_files.append(md_file)
    
    return blog_files


def import_blogs():
    """主导入函数"""
    print("=" * 60)
    print("导入现有博客到Chroma向量库")
    print("=" * 60)
    
    # 初始化向量库
    print("\n[1/4] 初始化Chroma向量库...")
    vector_store = VectorStore()
    print(f"  - Collection: {vector_store.collection_name}")
    
    # 获取博客目录
    blog_dir = config.BLOG_SOURCE_DIR
    print(f"\n[2/4] 扫描博客目录: {blog_dir}")
    
    if not blog_dir.exists():
        print(f"  错误: 博客目录不存在: {blog_dir}")
        return
    
    # 获取所有博客文件
    blog_files = get_all_blog_files(blog_dir)
    print(f"  - 找到 {len(blog_files)} 篇博客文章")
    
    # 准备批量导入数据 (限制前20篇用于测试)
    print("\n[3/4] 解析博客内容...")
    ids = []
    documents = []
    metadatas = []
    
    # 限制测试数量
    max_test = 20
    
    for i, md_file in enumerate(blog_files):
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  警告: 无法读取 {md_file}: {e}")
            continue
        
        # 解析front matter
        metadata, body = parse_front_matter(content)
        
        # 提取标题
        title = metadata.get('title', '') or extract_title_from_content(body)
        
        # 生成ID (使用slug或文件名)
        slug = metadata.get('slug', '') or md_file.stem
        doc_id = slug[:100]  # 限制ID长度
        
        # 构建要存储的文档 (标题 + 内容摘要)
        # 截取部分内容避免过长
        content_preview = body[:2000] if len(body) > 2000 else body
        
        # 合并标题和内容作为完整文档
        full_document = f"{title}\n\n{content_preview}"
        
        # 构建metadata
        doc_metadata = {
            'slug': slug,
            'title': title[:200] if title else 'untitled',
            'date': metadata.get('date', ''),
            'lang': metadata.get('lang', 'zh'),
            'author': metadata.get('author', ''),
            'tags': metadata.get('tags', ''),
            'description': metadata.get('description', '')[:500],
            'filepath': str(md_file.relative_to(blog_dir)),
        }
        
        ids.append(doc_id)
        documents.append(full_document)
        metadatas.append(doc_metadata)
        
        if (i + 1) % 10 == 0:
            print(f"  - 已解析 {i + 1}/{len(blog_files)} 篇")
    
    print(f"  - 解析完成: {len(ids)} 篇")
    
    # 导入到向量库
    print("\n[4/4] 导入到Chroma向量库...")
    
    existing_docs = vector_store.get_all_documents(limit=1)
    if existing_docs:
        print("  - 清空现有collection并重新导入...")
        vector_store.delete_collection()
        vector_store._init_collection()
    
    total_imported = 0
    failed = []
    import time
    
    # 逐个导入
    for i, (doc_id, doc, meta) in enumerate(zip(ids, documents, metadatas)):
        max_retries = 5
        for attempt in range(max_retries):
            try:
                vector_store.add_documents([doc_id], [doc], [meta])
                total_imported += 1
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                failed.append((doc_id, str(e)[:100]))
        
        if (i + 1) % 20 == 0:
            print(f"  - 进度: {i + 1}/{len(ids)} (成功: {total_imported}, 失败: {len(failed)})")
    
    print(f"\n导入完成! 共导入 {total_imported} 篇博客到向量库")
    
    if failed:
        print(f"  警告: {len(failed)} 篇导入失败:")
        for doc_id, err in failed[:5]:
            print(f"    - {doc_id}: {err[:50]}")
    
    print(f"\n导入完成! 共导入 {total_imported} 篇博客到向量库")
    
    # 验证
    print("\n[验证] 测试搜索功能...")
    test_queries = ["糖尿病饮食", "血糖控制"]
    
    for query in test_queries:
        results = vector_store.search(query, n_results=3)
        if results and results.get('documents') and results['documents'][0]:
            print(f"\n  查询: '{query}'")
            for i, doc in enumerate(results['documents'][0]):
                title = results['metadatas'][0][i].get('title', 'N/A')[:50] if results.get('metadatas') else 'N/A'
                dist = results['distances'][0][i] if results.get('distances') else 0
                print(f"    {i+1}. {title} (距离: {dist:.3f})")
        else:
            print(f"  查询 '{query}' 无结果")
    
    print("\n" + "=" * 60)
    print("导入完成!")
    print("=" * 60)


if __name__ == "__main__":
    import_blogs()
