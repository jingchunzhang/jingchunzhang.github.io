import os
import subprocess
from pathlib import Path
from datetime import datetime
import config

class Publisher:
    def __init__(self, repo_path: str = None):
        self.repo_path = Path(repo_path) if repo_path else config.PROJECT_ROOT
    
    def create_blog_post(self, slug: str, content: str, front_matter: str, subdir: str = None) -> Path:
        file_path = self.repo_path / "blog"
        
        if subdir:
            file_path = file_path / subdir / f"{slug}.md"
        else:
            file_path = file_path / f"{slug}.md"
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        full_content = front_matter + content
        file_path.write_text(full_content, encoding='utf-8')
        
        print(f"已创建文章: {file_path}")
        return file_path
    
    def git_add_commit_push(self, message: str = None):
        """Git add -> commit -> push"""
        if message is None:
            message = f"Auto publish: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        try:
            # git add
            subprocess.run(["git", "add", "-A"], cwd=self.repo_path, check=True)
            
            # git status 检查是否有更改
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if not result.stdout.strip():
                print("没有需要提交的更改")
                return False
            
            # git commit
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_path,
                check=True
            )
            
            # git push
            subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=self.repo_path,
                check=True
            )
            
            print("已推送到 GitHub")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Git 操作失败: {e}")
            return False
    
    def get_existing_slugs(self) -> set:
        """获取已存在的博客文章 slug"""
        slugs = set()
        blog_dir = self.repo_path / "blog"
        
        if not blog_dir.exists():
            return slugs
        
        for md_file in blog_dir.glob("**/*.md"):
            # 读取文件获取 slug
            content = md_file.read_text(encoding='utf-8')
            if content.startswith('---'):
                lines = content.split('---')
                if len(lines) >= 2:
                    fm = lines[1]
                    for line in fm.split('\n'):
                        if line.startswith('slug:'):
                            slug = line.split(':', 1)[1].strip()
                            slugs.add(slug)
                            break
        
        return slugs
