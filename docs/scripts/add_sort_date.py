import glob
import re
import os
import yaml

def add_sort_date():
    files = glob.glob('blog/**/*.md', recursive=True)
    pattern = re.compile(r'^(date:.*?)$', re.MULTILINE)
    
    count = 0
    for f in files:
        if os.path.isdir(f): continue
        try:
            with open(f, 'r') as file:
                content = file.read()
            
            if not content.startswith('---'):
                continue
                
            parts = content.split('---', 2)
            if len(parts) < 3:
                continue
                
            frontmatter_raw = parts[1]
            try:
                fm = yaml.safe_load(frontmatter_raw)
            except:
                continue
                
            if not fm or 'date' not in fm:
                continue
            
            if 'sort_date' in fm:
                continue

            date_val = str(fm['date'])
            
            def replacer(match):
                original = match.group(1)
                return f"{original}\nsort_date: \"{date_val}\""
            
            new_frontmatter = pattern.sub(replacer, frontmatter_raw, count=1)
            
            new_content = f"---{new_frontmatter}---{parts[2]}"
            
            if new_content != content:
                with open(f, 'w') as file:
                    file.write(new_content)
                count += 1
                
        except Exception as e:
            print(f"Error processing {f}: {e}")
            
    print(f"Added sort_date to {count} files.")

if __name__ == "__main__":
    add_sort_date()