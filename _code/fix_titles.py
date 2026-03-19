#!/usr/bin/env python3
"""
Fix markdown titles in front matter based on multiple criteria.
"""

import os
import re
import sys
from pathlib import Path


def extract_front_matter(content):
    """Extract YAML front matter from markdown content."""
    if not content.startswith("---"):
        return None, content
    
    # Find the closing ---
    end_match = re.search(r"^---\s*$", content[3:], re.MULTILINE)
    if not end_match:
        return None, content
    
    front_matter_end = 3 + end_match.start()
    front_matter = content[3:front_matter_end]
    body = content[front_matter_end + 3:].lstrip("\n")
    
    return front_matter, body


def parse_title_from_frontmatter(front_matter):
    """Extract title from YAML front matter."""
    if not front_matter:
        return None
    
    match = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", front_matter, re.MULTILINE)
    if match:
        return match.group(1).strip('"\'')
    return None


def needs_fixing(title, filename_slug):
    """Check if title needs fixing based on criteria."""
    if not title:
        return False
    
    # Criteria 1: Starts with lowercase letter (and is not just a number)
    if title and title[0].islower() and not title[0].isdigit():
        return True
    
    # Criteria 2: Contains certain phrases (case insensitive)
    phrases = ["feasibility of", "analysis of", "study of", "effect of"]
    if any(phrase in title.lower() for phrase in phrases):
        return True
    
    # Criteria 3: Longer than 80 characters
    if len(title) > 80:
        return True
    
    # Criteria 4: Identical to filename slug
    if title.lower() == filename_slug.lower():
        return True
    
    return False


def extract_h1_from_body(body):
    """Extract the first H1 heading from markdown body."""
    for line in body.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return None


def update_front_matter_title(front_matter, new_title):
    """Update the title in front matter."""
    # Match title with optional quotes
    pattern = r"^title:\s*['\"]?(.+?)['\"]?\s*$"
    replacement = f'title: "{new_title}"'
    
    updated = re.sub(pattern, replacement, front_matter, flags=re.MULTILINE)
    return updated


def process_markdown_file(file_path):
    """Process a single markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    front_matter, body = extract_front_matter(content)
    if not front_matter:
        return None
    
    old_title = parse_title_from_frontmatter(front_matter)
    if not old_title:
        return None
    
    filename_slug = file_path.stem
    
    if not needs_fixing(old_title, filename_slug):
        return None
    
    new_title = extract_h1_from_body(body)
    if not new_title:
        return None
    
    # If new title is the same, skip
    if new_title == old_title:
        return None
    
    # Update front matter
    updated_front_matter = update_front_matter_title(front_matter, new_title)
    updated_content = f"---\n{updated_front_matter}\n---\n{body}"
    
    # Write back
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    return (old_title, new_title)


def main():
    """Main entry point."""
    # Determine base path
    current_dir = Path.cwd()
    blog_dir = None
    
    # Check for docs/blog/ or blog/
    if (current_dir / "docs" / "blog").exists():
        blog_dir = current_dir / "docs" / "blog"
    elif (current_dir / "blog").exists():
        blog_dir = current_dir / "blog"
    else:
        print("Error: Could not find blog/ or docs/blog/ directory.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Scanning: {blog_dir}")
    
    fixed_count = 0
    for md_file in blog_dir.rglob("*.md"):
        result = process_markdown_file(md_file)
        if result:
            old_title, new_title = result
            rel_path = md_file.relative_to(current_dir)
            print(f"Fixed: {rel_path} | Old: {old_title} -> New: {new_title}")
            fixed_count += 1
    
    print(f"\nTotal fixed: {fixed_count}")


if __name__ == "__main__":
    main()
