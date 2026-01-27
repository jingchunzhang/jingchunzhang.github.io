# 项目需求与上下文（req.md）

> 目的：让后续切换到其它大模型/agent时，无需重新通读整个仓库，也能快速理解本项目是什么、当前做到哪、下一步做什么、有哪些硬约束。

## 0. 重要约束（先读）

1. **req.md 与交互日志仅用于维护，不对普通博客用户可见**。
   - 本文件位于 `docs/_ai/`（以下路径均以 `docs/` 为站点根目录）。
   - `docs/_ai/` 不应被 Jekyll 发布；也不应提交到 git（本次需求：**不发布 + 仅本地**）。
2. **所有与 AI 的交互（输入/输出）需要记录到本目录**：`docs/_ai/interaction-log.md`。
   - 这是“让 AI 接着上次继续干活”的核心上下文来源。
3. **内容面向普通读者（糖尿病相关科普 + 个人记录），但维护文档/日志不面向读者**。
4. **不要把敏感信息放入可发布内容**。
   - 当前仓库的 `docs/_config.yml` 中存在 `gitalk.clientSecret`（疑似敏感）。若未来要开源/公开传播，建议尽快轮换或移除。

## 1. 项目概况

### 1.1 项目是什么

- 一个基于 **GitHub Pages / Jekyll** 的静态博客站点。
- 站点域名：`blog.tangyou.space`（见 `docs/CNAME`）。
- 站点定位（见 `docs/index.md`）：
  - `shop.tangyou.space` 的配套博客；
  - 主题为糖尿病管理（预防/治疗/康复），以及作者的个人健康日志与技术思考。

### 1.2 当前内容组织

- 已有核心板块：
  - 预防：`docs/prevention/`（含 diet/exercise/sleep/emotion 等子主题，且部分有英文版 `*-en.md`）
  - 诊断标准：`docs/diabetes-diagnostic-criteria.md`（含英文版）
  - 关于我：`docs/aboutme.md`（含英文版）
- 首页：`docs/index.md`（含英文版 `docs/index-en.md`）

### 1.3 站点功能

- 主题：`jekyll-theme-Cayman`（见 `docs/_config.yml`）。
- 站点插件：`jekyll-sitemap`、`jekyll-feed`（见 `docs/_config.yml`）。
- 自定义布局：
  - `docs/_layouts/default.html`：覆盖/扩展主题默认布局（包含语言切换 + 面包屑 + giscus 评论）。
  - `docs/_layouts/post.html`：文章布局（目前仅透传内容）。
- 面包屑：`docs/_includes/breadcrumb.html` + `docs/assets/css/breadcrumb.css`
  - 采用 URL path + case 映射标题的方式（硬编码映射）。
- 评论：当前布局使用 **giscus**（`docs/_layouts/default.html` 中嵌入脚本）。
  - `docs/_config.yml` 内仍有 `gitalk` 配置，但目前看不再使用（可能历史遗留）。

## 2. 需求（你我共同维护的“产品需求”）

### 2.1 总目标

1. 持续建设“糖友空间博客”内容体系：从**预防/治疗/康复**到个人记录。
2. 保持站点结构清晰：分类页（index）+ 主题深度文章 + 中英文对应。
3. 保持可维护性：任何新 agent 读完本文件即可接手。

### 2.2 内容侧需求（约定）

- 文章以 `Markdown` 编写，包含 Front Matter（layout/title/lang/translation_key/date/author 等）。
- 双语策略：
  - 中文：`xxx.md`
  - 英文：`xxx-en.md`
  - 索引页也有英文：如 `prevention/index.md` + `prevention/index-en.md`
- 目录索引页应维护到位：首页、`prevention/index.md` 等要能链接到新增文章。

### 2.3 工程侧需求（约定）

- Jekyll 本地可构建通过：至少 `bundle exec jekyll build` 无报错。
- 不把维护日志/需求文档发布给读者（本地可见，站点不可见）。
- 交互日志持续更新：保证“开终端说几句话，AI 能续上次的活”。

## 3. 运行与开发环境

### 3.1 技术栈

- Ruby + Bundler
- `github-pages` gem（锁定到 `github-pages (232)`，对应 `jekyll (3.10.0)`，见 `docs/Gemfile.lock`）

### 3.2 常用命令（在 `docs/` 目录执行）

```bash
# 安装依赖
bundle install

# 本地构建
bundle exec jekyll build

# 本地预览（常用）
bundle exec jekyll serve --livereload
```

> 注：仓库里存在 `docs/_site/`（本地 build 产物）。原则上不要手改；是否提交由仓库策略决定。

## 4. 目录结构（关键路径）

```text
docs/
  _config.yml
  Gemfile / Gemfile.lock
  _layouts/
    default.html      # 主布局（语言切换 + 面包屑 + giscus）
    post.html
  _includes/
    breadcrumb.html   # 面包屑组件（路径 case 映射）
  assets/css/
    breadcrumb.css
  prevention/
    index.md / index-en.md
    diet/...
    exercise/...
    sleep/...
    emotion/...
  _gemini/            # 旧的AI执行/设计日志（当前已存在）
  _ai/                # 本地维护文件（req.md、交互日志等；不发布、不提交）
```

## 5. 约束条件（必须遵守）

1. **维护文档/日志不发布**：所有维护材料放在 `docs/_ai/`。
2. **交互日志必须持续追加**：每次对话都写入 `docs/_ai/interaction-log.md`。
3. **避免泄露敏感信息**：尤其不要把 token/secret 写到可发布页面；并关注 `docs/_config.yml` 的历史遗留敏感字段。
4. **避免大改主题结构**：现有站点基于 Cayman + 少量覆盖，优先小步迭代。

## 6. 当前工作进展（Snapshot）

### 6.1 已完成

- 站点基础搭建（Jekyll + Cayman）。
- 预防专区结构已搭建，并有部分深度文章（含中英文）。
- 面包屑导航已实现并接入主布局（详见：`docs/_gemini/20260115-breadcrumb-nav-implementation.md`）。
- 睡眠模块文章与索引已补齐（详见：`docs/_gemini/sleep-article/execution-log.md`）。

### 6.2 当前问题/风险（已知）

- `docs/_config.yml` 里包含 `gitalk.clientSecret`：
  - 若该 secret 真实有效，存在泄露风险；建议后续处理（轮换/移除/改用 giscus-only）。
- 面包屑映射是硬编码 case：新增目录时需要同步维护，否则会出现英文目录名或不理想标题。

## 7. 后续工作计划（建议路线图）

> 这部分是“未来 agent 的下一步”，可按优先级逐条推进。

### P0（保证可持续接力）

1. 固化“交互日志追加流程”（见下节）。
2. 每次完成一项工作后，在本文件的“当前工作进展”里更新 snapshot（只写结论+路径）。

### P1（内容体系补齐）

1. 建立 `treatment/`、`rehabilitation/` 主索引页，并从首页挂入口。
2. 补齐 `emotion/` 子模块索引与核心文章（中文/英文按需要）。

### P2（工程与体验优化）

1. 把面包屑路径标题映射迁移到 `_config.yml` 或数据文件（如 `_data/breadcrumb.yml`），避免硬编码。
2. 统一 i18n/语言切换策略（当前是基于 page.lang 的简单链接）。
3. 清理/确认评论系统：决定保留 giscus 还是 gitalk，并移除无用配置。

## 8. 交互日志与“继续上一次工作”的约定

### 8.1 日志文件

- 路径：`docs/_ai/interaction-log.md`
- 追加规则：
  - 每次对话追加一个 block：时间、参与者（user/assistant）、内容。
  - 只记录你我维护相关信息；不要记录任何隐私/敏感凭证。

### 8.2 未来 agent 的启动指令（建议）

当你切换模型/agent 后，第一句话建议类似：

> 请先阅读 docs/_ai/req.md 与 docs/_ai/interaction-log.md，并从日志最后的“Next step”继续。
