import os
import re

pattern = r'https://source\.unsplash\.com/[^)\s]+'
replacement_url = 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1200&q=80'
scan_dir = 'blog'

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, count = re.subn(pattern, replacement_url, content)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Replaced {count} occurrences in {filepath}")
        return count
    return 0

def main():
    total_replaced = 0
    file_count = 0
    
    for root, dirs, files in os.walk(scan_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                count = replace_in_file(filepath)
                if count > 0:
                    total_replaced += count
                    file_count += 1
    
    print(f"\nTotal: Replaced {total_replaced} occurrences in {file_count} files.")

if __name__ == '__main__':
    main()
