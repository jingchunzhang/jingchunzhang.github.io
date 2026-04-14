import os
import re

# Configuration
BLOG_ROOT = 'blog/diabetes'

# Pretty name mapping
NAME_MAP = {
    'complications': ('并发症', 'Complications'),
    'prevention': ('预防', 'Prevention'),
    'rehabilitation': ('康复', 'Rehabilitation'),
    'research': ('研究', 'Research'),
    'treatment': ('治疗', 'Treatment'),
    'diet': ('饮食', 'Diet'),
    'emotion': ('情绪与压力', 'Emotion & Stress'),
    'exercise': ('运动', 'Exercise'),
    'sleep': ('睡眠', 'Sleep'),
    'basics': ('基础知识', 'Basics'),
    'caregiver': ('护理者', 'Caregiver'),
    'monitoring': ('监测', 'Monitoring'),
    'topics': ('专题', 'Topics'),
    'diabetes': ('糖尿病', 'Diabetes')
}

def get_pretty_name(name, lang='zh'):
    if name in NAME_MAP:
        return NAME_MAP[name][0] if lang == 'zh' else NAME_MAP[name][1]
    if re.match(r'\d{4}-\d{2}', name):
        return name
    return name.capitalize()

def get_file_title(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^title:\s*["\']?(.*?)["\']?$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
    except:
        pass
    # Fallback to filename
    name = os.path.basename(file_path).replace('.md', '')
    # Remove leading date YYYY-MM-DD-
    name = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', name)
    return name.replace('-', ' ').capitalize()

def generate_index_content(dir_path, subdirs, files, lang='zh'):
    dir_name = os.path.basename(dir_path)
    pretty_name = get_pretty_name(dir_name, lang)
    
    title = f"{pretty_name}"
    content = f"---\nlayout: default\ntitle: {title}\nlang: {'zh' if lang == 'zh' else 'en'}\n---\n\n# {title}\n\n"
    
    if subdirs:
        content += "## 子分类\n" if lang == 'zh' else "## Subcategories\n"
        for d in sorted(subdirs):
            link = f"{d}/" if lang == 'zh' else f"{d}/index-en"
            content += f"*   [{get_pretty_name(d, lang)}]({link})\n"
        content += "\n"
    
    # Filter files by language
    if lang == 'zh':
        relevant_files = [f for f in files if not any(x in f for x in ['-en', '.en', '.zh-cn.', '.zh.'])]
    else:
        relevant_files = [f for f in files if '-en' in f or '.en' in f]
    
    if relevant_files:
        # Sort by filename descending (assuming it starts with YYYY-MM-DD)
        sorted_files = sorted(relevant_files, reverse=True)
        
        latest_files = sorted_files[:10]
        remaining_files = sorted_files[10:]
        
        if latest_files:
            content += "## 最新文章\n" if lang == 'zh' else "## Latest Articles\n"
            for f in latest_files:
                file_path = os.path.join(dir_path, f)
                file_title = get_file_title(file_path)
                content += f"*   [{file_title}]({f.replace('.md', '')})\n"
            content += "\n"
            
        if remaining_files:
            content += "## 所有文章\n" if lang == 'zh' else "## All Articles\n"
            for f in remaining_files:
                file_path = os.path.join(dir_path, f)
                file_title = get_file_title(file_path)
                content += f"*   [{file_title}]({f.replace('.md', '')})\n"
            content += "\n"
            
    # Include post-list at the bottom for filtering/styling if needed, 
    # but the user wanted the links in the index itself.
    # content += "\n---\n\n{% include post-list.html %}\n"
    return content

def main():
    for root, dirs, files in os.walk(BLOG_ROOT):
        # Exclude hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        md_files = [f for f in files if f.endswith('.md') and not f.startswith('index')]
        
        # Create index.md
        zh_content = generate_index_content(root, dirs, md_files, 'zh')
        with open(os.path.join(root, 'index.md'), 'w', encoding='utf-8') as f:
            f.write(zh_content)
            
        # Create index-en.md
        en_content = generate_index_content(root, dirs, md_files, 'en')
        with open(os.path.join(root, 'index-en.md'), 'w', encoding='utf-8') as f:
            f.write(en_content)
            
    print("Indexing complete.")

if __name__ == "__main__":
    main()
