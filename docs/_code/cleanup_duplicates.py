import os
import shutil
from pathlib import Path

BLOG_DIR = Path("docs/blog")
TRASH_DIR = BLOG_DIR / "_trash"
TRASH_DIR.mkdir(exist_ok=True)

def move_to_trash(file_path):
    if not file_path.exists():
        print(f"Not Found: {file_path}")
        return
    
    target_name = file_path.name
    target_path = TRASH_DIR / target_name
    
    # Handle naming collision in trash
    if target_path.exists():
        timestamp = os.path.getmtime(file_path)
        target_path = TRASH_DIR / f"{target_name}_{int(timestamp)}"
        
    shutil.move(str(file_path), str(target_path))
    print(f"Moved to Trash: {file_path}")

def fix_best_gifts_title():
    target_file = BLOG_DIR / "2026-03-14-the-best-gifts-for-people-with-diabetes.md"
    if not target_file.exists():
        print(f"Not Found: {target_file}")
        return

    with open(target_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    title_fixed = False
    h1_fixed = False
    
    NEW_TITLE = "糖尿病患者的最佳礼物清单：避坑指南与实用推荐"
    
    for line in lines:
        # Fix Front Matter Title
        if line.startswith("title: ") and not title_fixed:
            new_lines.append(f'title: "{NEW_TITLE}"\n')
            title_fixed = True
            continue
            
        # Fix H1 content
        if line.startswith("# ") and not h1_fixed:
            new_lines.append(f"# {NEW_TITLE}\n")
            h1_fixed = True
            continue
            
        new_lines.append(line)
        
    with open(target_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Fixed Title: {target_file}")

def main():
    print("Starting Cleanup...")
    
    # 1. Fix "Best Gifts"
    fix_best_gifts_title()
    
    # 2. Move Duplicates
    files_to_trash = [
        "prevention/diet/breakfast-meal-prep-diabetes-prevention.md",
        "prevention/diet/breakfast-meal-prep-diabetes-prevention-en.md",
        "prevention/diet/grocery-list-diabetes-meal-prep-prevention.md",
        "prevention/diet/grocery-list-diabetes-meal-prep-prevention-en.md",
        "prevention/diet/freezer-friendly-diabetes-dinners-prevention.md",
        "prevention/diet/freezer-friendly-diabetes-dinners-prevention-en.md",
        "prevention/diet/dessert-portion-meal-prep-diabetes-prevention.md",
        "prevention/diet/dessert-portion-meal-prep-diabetes-prevention-en.md",
        "treatment/diet/2026-03-15-pregnancy-diabetes-birth-guide.md",
        "treatment/diet/2026-03-15-pregnancy-diabetes-birth-guide-en.md",
        "treatment/emotion/2026-03-15-diabetes-supplies-rights.md",
        "treatment/emotion/2026-03-15-diabetes-supplies-rights-en.md",
        "2026-03-14-how-to-participate-in-diabetes-research-panels-and.md"
    ]
    
    for relative_path in files_to_trash:
        full_path = BLOG_DIR / relative_path
        move_to_trash(full_path)

    print("Cleanup Complete.")

if __name__ == "__main__":
    main()
