import os
import yaml
import glob
import datetime

def check_dates():
    files = glob.glob('blog/**/*', recursive=True)
    for f in files:
        if os.path.isdir(f): continue
        try:
            with open(f, 'r') as file:
                content = file.read()
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])
                        if frontmatter and 'date' in frontmatter:
                            date_val = frontmatter['date']
                            if isinstance(date_val, list):
                                print(f"Found ARRAY date: {f} -> {date_val}")
        except Exception:
            pass

if __name__ == "__main__":
    check_dates()