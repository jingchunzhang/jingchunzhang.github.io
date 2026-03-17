import os
import re
from pathlib import Path
import difflib

BLOG_DIR = Path("blog")

def is_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def count_chinese_ratio(text):
    if not text: return 0
    zh_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    return zh_chars / len(text)

def check_language_mismatch(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract front matter
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None # No front matter
    
    fm = match.group(1)
    lang_match = re.search(r'lang:\s*(\w+)', fm)
    lang = lang_match.group(1) if lang_match else None
    
    # Extract body (skip front matter)
    body = content[match.end():].strip()
    sample = body[:500]
    
    if not sample:
        return None

    zh_ratio = count_chinese_ratio(sample)
    
    filename = file_path.name
    is_en_file = filename.endswith("-en.md")
    
    issues = []
    
    if is_en_file:
        if zh_ratio > 0.1:
            issues.append(f"English filename but high Chinese content ({zh_ratio:.2%})")
        if lang == 'zh':
             issues.append(f"English filename but lang: zh in front matter")
    else:
        # Chinese file
        if zh_ratio < 0.05 and len(sample) > 50:
             issues.append(f"Chinese filename but low Chinese content ({zh_ratio:.2%})")
        if lang == 'en':
             issues.append(f"Chinese filename but lang: en in front matter")
             
    if issues:
        return "; ".join(issues)
    return None

def check_title_similarity(files):
    titles = []
    for p in files:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read(1000)
            # Match title: "..." or title: ...
            match = re.search(r'^title:\s*(["\']?)(.*?)\1\s*$', content, re.MULTILINE)
            if match:
                title = match.group(2).strip()
                # Skip if title is empty
                if title:
                    titles.append((p, title))
    
    # Compare
    seen = set()
    duplicates = []
    
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            p1, t1 = titles[i]
            p2, t2 = titles[j]
            
            # Skip if same file or already seen pair
            if p1 == p2: continue
            
            # Skip if one is EN and other is ZH of same article (e.g. title vs title-en)
            # Usually EN title is different, but if they are close, it might be okay?
            # Actually we look for *unintended* duplicates.
            
            # Simple check: identical titles
            if t1 == t2:
                duplicates.append(f"Identical Title: '{t1}' in {p1.name} and {p2.name}")
                continue
                
            # Fuzzy check
            ratio = difflib.SequenceMatcher(None, t1, t2).ratio()
            if ratio > 0.9 and len(t1) > 10:
                 duplicates.append(f"Similar Title (ratio={ratio:.2f}): '{t1}' vs '{t2}' in {p1.name} and {p2.name}")

    return duplicates

def main():
    all_files = list(BLOG_DIR.rglob("*.md"))
    all_files = [f for f in all_files if "_trash" not in str(f)]
    
    print(f"Scanning {len(all_files)} files...")
    
    # 1. Language Mismatch
    print("\n--- Language Mismatches ---")
    mismatches = []
    for f in all_files:
        res = check_language_mismatch(f)
        if res:
            print(f"{f}: {res}")
            mismatches.append(f)
            
    if not mismatches:
        print("None found.")

    # 2. Title Similarity
    print("\n--- Title Duplicates ---")
    dupes = check_title_similarity(all_files)
    for d in dupes:
        print(d)
    if not dupes:
        print("None found.")

if __name__ == "__main__":
    main()
