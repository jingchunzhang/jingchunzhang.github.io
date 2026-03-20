import os
import yaml
import re
import argparse
import sys

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
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        body = match.group(2)
        try:
            fm = yaml.safe_load(fm_text)
            return fm, body, fm_text
        except yaml.YAMLError:
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

    for root, dirs, files in os.walk(BLOG_DIR):
        for file in files:
            if not file.endswith('.md'):
                continue

            filepath = os.path.join(root, file)
            fm, body, original_fm_text = load_frontmatter(filepath)

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
            else:
                 pass

    print(f"\nTotal files updated: {updated_count}")

def generate_tag_data():
    all_tags = {}

    for root, dirs, files in os.walk(BLOG_DIR):
        for file in files:
            if not file.endswith('.md'):
                continue

            filepath = os.path.join(root, file)
            fm, body, _ = load_frontmatter(filepath)

            if fm and 'tags' in fm:
                tags = fm['tags']
                if isinstance(tags, str):
                    tags = [tags]
                for tag in tags:
                    all_tags[tag] = all_tags.get(tag, 0) + 1

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(all_tags, f, default_flow_style=False, allow_unicode=True)

    print(f"Generated {DATA_FILE} with {len(all_tags)} unique tags.")
    for tag, count in sorted(all_tags.items(), key=lambda x: x[1], reverse=True):
        print(f"- {tag}: {count}")

def main():
    parser = argparse.ArgumentParser(description='Manage blog tags')
    parser.add_argument('--scan', action='store_true', help='Scan and auto-tag posts based on directory')
    parser.add_argument('--list', action='store_true', help='List all tags and generate _data/tags.yml')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without saving')

    args = parser.parse_args()

    if args.scan:
        scan_and_update(dry_run=args.dry_run)
    
    if args.list:
        generate_tag_data()
    
    if not args.scan and not args.list:
        parser.print_help()

if __name__ == '__main__':
    main()
