import glob
import re
import os

def fix_dates():
    files = glob.glob('blog/**/*.md', recursive=True)
    pattern = re.compile(r'^date: (\d{4}-\d{2}-\d{2})\s*$', re.MULTILINE)
    
    count = 0
    for f in files:
        if os.path.isdir(f): continue
        try:
            with open(f, 'r') as file:
                content = file.read()
            
            new_content = pattern.sub(r'date: \1 00:00:00 +0800', content)
            
            if new_content != content:
                with open(f, 'w') as file:
                    file.write(new_content)
                count += 1
        except Exception as e:
            print(f"Error processing {f}: {e}")
            
    print(f"Updated dates in {count} files.")

if __name__ == "__main__":
    fix_dates()