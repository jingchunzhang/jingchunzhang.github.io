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
VOLCENGINE_EMBEDDING_MODEL = os.environ.get("VOLCENGINE_EMBEDDING_MODEL", "doubao-embedding-vision-251215")
VOLCENGINE_EMBEDDING_ENDPOINT = os.environ.get("VOLCENGINE_EMBEDDING_ENDPOINT", "https://ark.cn-beijing.volces.com/api/v3/embeddings/multimodal")

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

# 火山引擎LLM配置 (替代Gemini)
USE_VOLCENGINE_LLM = os.environ.get("USE_VOLCENGINE_LLM", "true").lower() == "true"
VOLCENGINE_LLM_API_BASE = os.environ.get("VOLCENGINE_LLM_API_BASE", "https://ark.cn-beijing.volces.com/api/v3")
VOLCENGINE_LLM_API_KEY = os.environ.get("VOLCENGINE_LLM_API_KEY", "54bf396f-61d1-4ef9-95d2-1da543cbd838")
VOLCENGINE_LLM_MODEL = os.environ.get("VOLCENGINE_LLM_MODEL", "doubao-seed-2-0-pro-260215")

# 内容配置
SIMILARITY_THRESHOLD = 0.8  # 相似度阈值，超过则拒绝
MIN_SIMILARITY_FOR_LINK = 0.4  # 用于自动内链的相似度阈值
DAILY_POST_LIMIT = 8  # 每日最大生成数量 (5-10篇)

# YMYL 领域配置
YMYL_DISCLAIMER = "本文由AI辅助生成，仅供信息参考，不构成医疗建议。请咨询专业医生后再做决策。"
BLOCKED_KEYWORDS = ["用药剂量", "自行停药", "擅自停药", "按我说的吃"]

# ============================================================
# 数据源配置
# ============================================================

# Ebook 配置
EBOOK_SOURCE_DIR = Path("/media/danezhang/Elements/seo/blog/ebook")
EBOOK_KEYWORDS = ["diabetes", "diabetic", "blood sugar", "glucose", "insulin", "糖尿病", "血糖"]

# RSS 订阅配置 (JSON格式，可配置多个源)
# 格式: [{"name": "源名称", "url": "RSS URL", "keywords": ["关键词过滤"]}]
RSS_SOURCES = [
    {"name": "Diabetes Strong", "url": "https://diabetesstrong.com/blog/feed/", "keywords": ["diabetes", "blood sugar", "diet"]},
    {"name": "Diabetes Journals", "url": "https://diabetesjournals.org/journals/pages/rss-feeds", "keywords": ["diabetes", "research"]},
    {"name": "BMJ Diabetes Research", "url": "https://drc.bmj.com/rss/recent.xml", "keywords": ["diabetes", "research"]},
]

# 爬虫配置 (可配置多个目标网站)
# 格式: [{"name": "源名称", "url": "基础URL", "keywords": ["关键词"], "selectors": {...}}]
SPIDER_SOURCES = [
    {
        "name": "Mayo Clinic Diabetes",
        "url": "https://www.mayoclinic.org/diseases-conditions/diabetes",
        "keywords": ["diabetes", "blood sugar", "treatment"],
        "selectors": {
            "article": "article",
            "title": "h1",
            "content": "div.content-body",
            "link": "a[href*='/diseases-conditions/']"
        }
    },
    {
        "name": "Healthline Diabetes",
        "url": "https://www.healthline.com/health/diabetes",
        "keywords": ["diabetes", "type 2", "blood glucose"],
        "selectors": {
            "article": "article",
            "title": "h1",
            "content": ".article-body",
            "link": "a[href*='/health/']"
        }
    },
]

# 数据源启用开关
ENABLE_EBOOK = os.environ.get("ENABLE_EBOOK", "true").lower() == "true"
ENABLE_RSS = os.environ.get("ENABLE_RSS", "true").lower() == "true"
ENABLE_SPIDER = os.environ.get("ENABLE_SPIDER", "true").lower() == "true"

# 爬虫配置
SPIDER_CONCURRENCY = int(os.environ.get("SPIDER_CONCURRENCY", "3"))
SPIDER_TIMEOUT = int(os.environ.get("SPIDER_TIMEOUT", "30"))
