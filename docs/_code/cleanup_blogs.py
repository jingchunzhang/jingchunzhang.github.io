import os
import re
import shutil
from pathlib import Path

BLOG_DIR = Path("../blog")
TRASH_DIR = BLOG_DIR / "_trash"
TRASH_DIR.mkdir(exist_ok=True, parents=True)

def parse_front_matter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        return match.group(1)
    return ""

def is_english_content(text):
    # Remove front matter first
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.DOTALL)
    # Check first 1000 chars to be fast
    sample = content[:1000]
    
    english_words = len(re.findall(r'\b(the|and|is|to|in|of|for|with)\b', sample.lower()))
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', sample))
    
    # If significantly more English structure words than Chinese chars, it's English
    if english_words > 10 and chinese_chars < 5:
        return True
    return False

def get_date_from_filename(filename):
    match = re.match(r'^(\d{4}-\d{2}-\d{2})-', filename)
    if match:
        return match.group(1)
    return "0000-00-00"

def get_normalized_key(filename):
    # Remove date prefix
    name_no_date = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename)
    return name_no_date

def cleanup():
    print("Starting cleanup...")
    print(f"Target Directory: {BLOG_DIR.absolute()}")
    
    all_files = []
    for root, dirs, files in os.walk(BLOG_DIR):
        if "_trash" in root: continue
        for file in files:
            if file.endswith(".md") and not file.startswith("."):
                all_files.append(Path(root) / file)
    
    print(f"Found {len(all_files)} markdown files.")
    
    # --- Step 1: Deduplicate (Date vs Non-Date, Old vs New) ---
    groups = {}
    for p in all_files:
        key = get_normalized_key(p.name)
        if key not in groups:
            groups[key] = []
        groups[key].append(p)

    for key, paths in groups.items():
        if len(paths) > 1:
            # Sort by date (descending), then by having date
            def sort_key(p):
                date_str = get_date_from_filename(p.name)
                has_date = 1 if date_str != "0000-00-00" else 0
                return (date_str, has_date)
            
            paths.sort(key=sort_key, reverse=True)
            
            keep = paths[0]
            remove = paths[1:]
            
            # Special check: ensure we don't delete files just because they have same name in different folders
            # IF content is different? No, key is filename. 
            # If 'index.md' exists in multiple folders, we should NOT dedup them!
            if key in ['index.md', 'index-en.md']:
                continue
                
            # Check if they are actually in different folders (e.g. prevention/diet/x.md vs treatment/diet/x.md)
            # If so, we might want to keep both OR delete one if it's a cross-category duplicate.
            # User said: "content duplication... same article in prevention/diet and treatment/diet"
            # So yes, we WANT to dedup across folders if filenames match.
            
            print(f"Duplicate group ({key}):")
            print(f"  Keeping: {keep.parent.name}/{keep.name}")
            for r in remove:
                print(f"  Moving to trash: {r.parent.name}/{r.name}")
                dest = TRASH_DIR / f"{r.parent.name}_{r.name}"
                shutil.move(str(r), dest)

    # --- Step 2: Language Mismatch Check ---
    # Re-scan valid files
    remaining_files = []
    for root, dirs, files in os.walk(BLOG_DIR):
        if "_trash" in root: continue
        for file in files:
            if file.endswith(".md") and not file.startswith("."):
                remaining_files.append(Path(root) / file)

    for p in remaining_files:
        if p.name == 'index.md' or p.name == 'index-en.md': continue
        
        # Check "Chinese" files (no -en suffix)
        if not p.name.endswith("-en.md"):
            try:
                content = p.read_text(encoding='utf-8')
                if is_english_content(content):
                    print(f"Language Mismatch (Expected ZH, found EN): {p.name}")
                    
                    # Check for sibling -en file
                    en_name = p.name.replace(".md", "-en.md")
                    # Also check dated version of en_name if p has date
                    
                    # If we renamed p to en_name, would it clash?
                    # Check if -en file exists in same folder
                    sibling_en = p.parent / en_name
                    
                    if sibling_en.exists():
                        print(f"  Target {en_name} already exists. Trashing mismatch file.")
                        shutil.move(str(p), TRASH_DIR / ("MISMATCH_" + p.name))
                    else:
                        # Check if maybe the -en file is in the trash (deleted as duplicate)?
                        # Or maybe it has a date and we don't?
                        # Normalized check
                        print(f"  Renaming to {en_name}")
                        p.rename(p.parent / en_name)
            except Exception as e:
                print(f"Error checking content of {p}: {e}")

    # --- Step 3: Fix Front Matter (Lang) ---
    print("Fixing metadata...")
    for root, dirs, files in os.walk(BLOG_DIR):
        if "_trash" in root: continue
        for file in files:
            if file.endswith(".md"):
                p = Path(root) / file
                try:
                    content = p.read_text(encoding='utf-8')
                    if not content.strip(): continue
                    
                    # Determine correct lang
                    if file.endswith("-en.md"):
                        lang = "en"
                    else:
                        lang = "zh"
                    
                    fm = parse_front_matter(content)
                    if not fm: continue
                    
                    if "lang:" not in fm:
                        print(f"  Adding lang: {lang} to {file}")
                        # Insert lang field
                        if re.search(r'^date:.*$', content, re.MULTILINE):
                            content = re.sub(r'(^date:.*$)', f'\\1\nlang: {lang}', content, count=1, flags=re.MULTILINE)
                        elif re.search(r'^title:.*$', content, re.MULTILINE):
                            content = re.sub(r'(^title:.*$)', f'\\1\nlang: {lang}', content, count=1, flags=re.MULTILINE)
                        else:
                            content = re.sub(r'^---\n', f'---\nlang: {lang}\n', content, count=1)
                        
                        p.write_text(content, encoding='utf-8')
                except Exception as e:
                    print(f"Error fixing metadata {p}: {e}")

if __name__ == "__main__":
    cleanup()
