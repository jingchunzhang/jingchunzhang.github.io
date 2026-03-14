"""
配置管理模块
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# ChromaDB 服务地址
CHROMA_HOST = os.environ.get("CHROMA_HOST", "http://localhost:8000")
CHROMA_COLLECTION = "blog_content"

# 向量库配置
USE_LOCAL_EMBEDDING = os.environ.get("USE_LOCAL_EMBEDDING", "true").lower() == "true"

# 火山引擎Embedding配置 (替代本地模型)
VOLCENGINE_EMBEDDING_API_BASE = os.environ.get("VOLCENGINE_API_BASE", "https://ark.cn-beijing.volces.com/api/v3")
VOLCENGINE_EMBEDDING_API_KEY = os.environ.get("VOLCENGINE_API_KEY", "54bf396f-61d1-4ef9-95d2-1da543cbd838")
VOLCENGINE_EMBEDDING_MODEL = os.environ.get("VOLCENGINE_EMBEDDING_MODEL", "doubao-embedding-vision-250615")
VOLCENGINE_EMBEDDING_ENDPOINT = os.environ.get("VOLCENGINE_EMBEDDING_ENDPOINT", "")

# ebook 资源路径
EBOOK_MANIFEST_DIR = PROJECT_ROOT / "_book" / "manifests"
EBOOK_TEMPLATES_DIR = PROJECT_ROOT / "_book" / "templates"
EBOOK_AUTHOR_CSV = PROJECT_ROOT / "_book" / "author-role-rotation.csv"

# 博客源文件目录
BLOG_SOURCE_DIR = PROJECT_ROOT / "blog"

# GitHub 配置
GITHUB_REPO = os.environ.get("GITHUB_REPO", "jingchunzhang/jingchunzhang.github.io")
GITHUB_BRANCH = os.environ.get("GITHUB_BRANCH", "main")

# LLM 配置
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"

# 内容配置
SIMILARITY_THRESHOLD = 0.8  # 相似度阈值，超过则拒绝
MIN_SIMILARITY_FOR_LINK = 0.4  # 用于自动内链的相似度阈值
DAILY_POST_LIMIT = 5  # 每日最大生成数量

# YMYL 领域配置
YMYL_DISCLAIMER = "本文由AI辅助生成，仅供信息参考，不构成医疗建议。请咨询专业医生后再做决策。"
BLOCKED_KEYWORDS = ["用药剂量", "停药", "处方", "治疗方案"]
