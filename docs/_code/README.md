# Blog Content Automation

## 目录结构

```
_code/
├── config.py           # 配置文件
├── main.py             # 每日任务入口
├── requirements.txt    # 依赖
├── src/
│   ├── chroma_client.py       # ChromaDB 连接
│   ├── vector_store.py        # 向量存储与检索
│   ├── ebook_loader.py        # Ebook 资源加载
│   ├── prompt_pool.py         # Prompt 变异池
│   ├── content_generator.py   # 内容生成
│   └── publisher.py           # Git 发布
└── data/               # 数据目录（预留）
```

## 环境准备

```bash
# 1. 安装依赖
cd _code
pip install -r requirements.txt

# 2. 配置环境变量
export GEMINI_API_KEY="your-api-key"
export CHROMA_HOST="http://localhost:8000"

# 3. 启动 ChromaDB 服务
# （你已经在 http://localhost:8000 启动了）
```

## 每日任务流程

1. **启动 ChromaDB**（你负责）
2. **运行任务**：`python _code/main.py`

## 核心功能

### 1. 向量检索防重复
- 每次生成前先查向量库
- 相似度 > 80% 则跳过或改写

### 2. Prompt 变异池
- 5 种体裁：对比清单、Step-by-step教程、避坑指南、选购指南、经验分享
- 4 种视角：预算型、资深糖友、医学研究者、营养师
- 随机组合，每次生成不同风格

### 3. Ebook 资源利用
- 从 `_book/manifests/` 读取选题
- 自动提取搜索意图、博客路径、下载链接

### 4. YMYL 安全护栏
- 自动插入免责声明
- 拦截敏感关键词（用药剂量等）
- 聚焦生活方式内容

### 5. 自动发布
- 生成 Markdown 文件
- Git add -> commit -> push
- 触发 GitHub Pages 构建

## 配置项

在 `config.py` 中可调整：
- `SIMILARITY_THRESHOLD`: 相似度阈值（默认0.8）
- `DAILY_POST_LIMIT`: 每日生成上限（默认5）
- `CHROMA_HOST`: ChromaDB 地址

## 使用方式

每天上午我执行任务时，运行：
```bash
cd /home/danezhang/dev/blog/jingchunzhang.github.io
python _code/main.py
```

前提：
1. ChromaDB 服务运行中（http://localhost:8000）
2. GEMINI_API_KEY 已配置
