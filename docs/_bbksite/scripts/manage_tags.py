import os
import yaml
import re
import argparse
import sys
import glob

BLOG_DIR = 'blog'
DATA_FILE = '_data/tags.yml'

TAG_MAPPING = {
    'prevention': 'Prevention',
    'treatment': 'Treatment',
    'rehabilitation': 'Rehabilitation',
    'diet': 'Diet',
    'exercise': 'Exercise',
    'sleep': 'Sleep',
    'emotion': 'Emotion',
    'health-log': 'Health Log',
    'tech-thoughts': 'Tech Thoughts',
    'products': 'Products',
    'seo': 'SEO',
    'affiliate': 'Affiliate'
}

def load_frontmatter(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None, None, None

    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        body = match.group(2)
        try:
            fm = yaml.safe_load(fm_text)
            return fm, body, fm_text
        except yaml.YAMLError:
            print(f"YAML Error in {filepath}")
            return None, content, None
    return None, content, None

def save_file(filepath, fm, body):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.dump(fm, f, default_flow_style=False, allow_unicode=True)
        f.write('---\n')
        f.write(body)

def get_tags_from_path(filepath):
    rel_path = os.path.relpath(filepath, BLOG_DIR)
    parts = rel_path.split(os.sep)
    tags = []

    for part in parts[:-1]:
        if part in TAG_MAPPING:
            tags.append(TAG_MAPPING[part])
        elif part not in ['index.md', 'index-en.md', '_trash']:
             clean_part = part.replace('-', ' ').title()
             tags.append(clean_part)

    return list(set(tags))

def scan_and_update(dry_run=False):
    updated_count = 0
    print("Scanning directory structure to update tags...")

    for root, dirs, files in os.walk(BLOG_DIR):
        for file in files:
            if not file.endswith('.md'):
                continue

            filepath = os.path.join(root, file)
            fm, body, _ = load_frontmatter(filepath)

            if fm is None:
                continue

            current_tags = fm.get('tags', [])
            if isinstance(current_tags, str):
                current_tags = [current_tags]
            
            path_tags = get_tags_from_path(filepath)
            
            new_tags = list(set(current_tags + path_tags))
            
            if set(new_tags) != set(current_tags):
                if dry_run:
                    print(f"[DRY RUN] Would update {filepath}: {current_tags} -> {new_tags}")
                else:
                    fm['tags'] = new_tags
                    save_file(filepath, fm, body)
                    print(f"Updated {filepath}: {new_tags}")
                    updated_count += 1
    
    print(f"\nTotal files updated: {updated_count}")

def generate_tag_data():
    all_tags = {}
    print("Generating _data/tags.yml...")

    for root, dirs, files in os.walk(BLOG_DIR):
        for file in files:
            if not file.endswith('.md'):
                continue

            filepath = os.path.join(root, file)
            fm, _, _ = load_frontmatter(filepath)

            if fm and 'tags' in fm:
                tags = fm['tags']
                if isinstance(tags, str):
                    tags = [tags]
                if tags:
                    for tag in tags:
                        all_tags[tag] = all_tags.get(tag, 0) + 1

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(all_tags, f, default_flow_style=False, allow_unicode=True)

    print(f"Generated {DATA_FILE} with {len(all_tags)} unique tags.")
    for tag, count in sorted(all_tags.items(), key=lambda x: x[1], reverse=True):
        print(f"- {tag}: {count}")

def manage_tags(action, tag, file_pattern=None, new_tag=None, dry_run=False):
    updated_count = 0
    
    if file_pattern:
        if '**' in file_pattern:
            files = glob.glob(file_pattern, recursive=True)
        else:
            files = glob.glob(file_pattern)
        
        files = [f for f in files if f.endswith('.md') and BLOG_DIR in f]
    else:
        files = []
        for root, dirs, filenames in os.walk(BLOG_DIR):
            for f in filenames:
                if f.endswith('.md'):
                    files.append(os.path.join(root, f))

    print(f"Processing {len(files)} files for action: {action}")

    for filepath in files:
        fm, body, _ = load_frontmatter(filepath)
        if fm is None:
            continue

        current_tags = fm.get('tags', [])
        if isinstance(current_tags, str):
            current_tags = [current_tags]
        
        current_tags = list(current_tags) if current_tags else []
        original_tags = current_tags.copy()
        modified = False

        if action == 'add':
            if tag not in current_tags:
                current_tags.append(tag)
                modified = True
        
        elif action == 'remove':
            if tag in current_tags:
                current_tags.remove(tag)
                modified = True
        
        elif action == 'rename':
            if tag in current_tags and new_tag:
                current_tags = [new_tag if t == tag else t for t in current_tags]
                current_tags = list(set(current_tags))
                modified = True

        if modified:
            if dry_run:
                print(f"[DRY RUN] {filepath}: {original_tags} -> {current_tags}")
            else:
                fm['tags'] = current_tags
                save_file(filepath, fm, body)
                print(f"Updated {filepath}: {original_tags} -> {current_tags}")
                updated_count += 1
    
    print(f"Total files updated: {updated_count}")
    
    if not dry_run and updated_count > 0:
        generate_tag_data()

def main():
    parser = argparse.ArgumentParser(description='Manage blog tags')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    parser_scan = subparsers.add_parser('scan', help='Scan directory structure and auto-populate tags')
    parser_scan.add_argument('--dry-run', action='store_true')

    parser_list = subparsers.add_parser('list', help='List all tags and regenerate data file')

    parser_add = subparsers.add_parser('add', help='Add a tag to specific files')
    parser_add.add_argument('tag', help='Tag to add')
    parser_add.add_argument('file_pattern', help='Glob pattern for files (e.g. "blog/posts/*.md")')
    parser_add.add_argument('--dry-run', action='store_true')

    parser_remove = subparsers.add_parser('remove', help='Remove a tag from specific files')
    parser_remove.add_argument('tag', help='Tag to remove')
    parser_remove.add_argument('file_pattern', help='Glob pattern for files')
    parser_remove.add_argument('--dry-run', action='store_true')

    parser_rename = subparsers.add_parser('rename', help='Rename a tag globally')
    parser_rename.add_argument('old_tag', help='Old tag name')
    parser_rename.add_argument('new_tag', help='New tag name')
    parser_rename.add_argument('--dry-run', action='store_true')

    args = parser.parse_args()

    if args.command == 'scan':
        scan_and_update(dry_run=args.dry_run)
        generate_tag_data()
    elif args.command == 'list':
        generate_tag_data()
    elif args.command == 'add':
        manage_tags('add', args.tag, file_pattern=args.file_pattern, dry_run=args.dry_run)
    elif args.command == 'remove':
        manage_tags('remove', args.tag, file_pattern=args.file_pattern, dry_run=args.dry_run)
    elif args.command == 'rename':
        manage_tags('rename', args.old_tag, new_tag=args.new_tag, dry_run=args.dry_run)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
