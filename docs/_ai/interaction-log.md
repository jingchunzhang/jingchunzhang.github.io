# AI 交互日志（本地维护，不发布）

> 目的：记录你我与 AI 的所有输入/输出，让后续更换模型/agent时可以“接着上次继续干”。

---

## 记录格式约定

每次对话按如下结构追加：

```text
## YYYY-MM-DD HH:MM (TZ)

### User
<原始输入>

### Assistant
<原始输出>

### Next step
<下一步一句话指令，供下个agent接力>
```

---

## 2026-01-27 11:20 (Asia/Shanghai)

### User
请你阅读本项目, 写一个本项目的概况,需求,约束条件,运行环境等描述性文档,req.md. 后续我会切换其它大模型或者agent开继续本项目,希望其他模型通过阅读req.md很快了解本项目的上下文,需求,约束条件,进尔很快开展工作,而不是重新阅读一遍本项目所有文档.   我再描述一遍我的需求,我希望后续我打开终端,说几句话,AI就能继续上一次的工作.  请根据以上情况和项目情况, 给我整理文档,包括前面提到的req.md,也包括后续工作计划,当前工作进展.   我跟你所有的交互,输入输出,请记录到本地本目录下.以上所有要展示给普通blog用户看,仅仅是你和我来维护.

### Assistant
（已创建 `docs/_ai/req.md` 与本日志文件；并确认：维护文档/日志“不发布+仅本地”。）

### Next step
在后续每次交互后，追加一段日志；若需要进一步工程化，可加入脚本自动把终端会话附加到本文件。

---

## 2026-01-27 11:28 (Asia/Shanghai)

### User
请给糖尿病治疗,糖尿病康复,个人健康日志,技术个人思考几个子栏目添加index.md,避免404

### Assistant
已新增以下栏目索引页（同时补齐英文索引，避免语言切换时 404），并更新面包屑标题映射：

- `docs/treatment/index.md`
- `docs/treatment/index-en.md`
- `docs/rehabilitation/index.md`
- `docs/rehabilitation/index-en.md`
- `docs/health-log/index.md`
- `docs/health-log/index-en.md`
- `docs/tech-thoughts/index.md`
- `docs/tech-thoughts/index-en.md`
- `docs/_includes/breadcrumb.html`：新增 treatment/rehabilitation/health-log/tech-thoughts 的显示标题映射

### Next step
如需把这些新栏目入口加到首页/导航（或完善英文语言切换逻辑），继续下发具体需求即可。

---

## 2026-03-02 11:55 (Asia/Shanghai)

### User
What did we do so far?

Continue if you have next steps, or stop and ask for clarification if you are unsure how to proceed.

### Assistant
- 先复核 `docs/_ai/req.md` 与 `docs/_ai/interaction-log.md` 的约束：维护文件不发布、交互日志持续追加；不运行 bundle；只写 md。
- 修复康复-运动索引的占位：
  - `docs/blog/rehabilitation/exercise/index.md`：把“（待添加）”替换为实际文章链接，并补上 `相关阅读` + `{% include related-articles.html %}`。
  - `docs/blog/rehabilitation/exercise/index-en.md`：把 “(Coming soon)” 替换为实际文章链接。
- 更新预防-饮食索引：
  - `docs/blog/prevention/diet/index.md`：新增 UPF 文章链接与一句话简介。
  - `docs/blog/prevention/diet/index-en.md`：新增 UPF 文章链接与一句话简介。
  - `docs/blog/prevention/diet/index.md`：补上 `相关阅读` + `{% include related-articles.html %}`，并把两个“相关阅读”小节分别标注为“内链/站内推荐”。

### Next step
继续做内容体系补齐：优先检查各栏目 index(-en).md 是否漏链/占位，并在每次修改后同步追加本日志。

---

## 2026-03-02 12:35 (Asia/Shanghai)

### User
What did we do so far?

Continue if you have next steps, or stop and ask for clarification if you are unsure how to proceed.

### Assistant
- 复核 `docs/_ai/req.md` 约束与站点机制（面包屑映射在 `docs/_includes/breadcrumb.html`；推荐逻辑在 `docs/_includes/related-articles.html` 依赖 `translation_key` 与 `lang`）。
- 在正确的站点仓库路径下新增 10 组中英双语文章（20 个 md 文件），覆盖四个主题：
  - diet（4 组）：
    - `docs/blog/prevention/diet/breakfast-structure-diabetes-prevention.md` + `...-en.md`
    - `docs/blog/prevention/diet/protein-strategy-glucose-stability.md` + `...-en.md`
    - `docs/blog/prevention/diet/hydration-glucose-stability.md` + `...-en.md`
    - `docs/blog/prevention/diet/intermittent-fasting-diabetes-prevention.md` + `...-en.md`
  - exercise（2 组）：
    - `docs/blog/prevention/exercise/post-meal-walk-glucose-control.md` + `...-en.md`
    - `docs/blog/prevention/exercise/strength-training-insulin-sensitivity.md` + `...-en.md`
  - sleep（2 组）：
    - `docs/blog/prevention/sleep/sleep-regularity-social-jetlag.md` + `...-en.md`
    - `docs/blog/prevention/sleep/caffeine-sleep-glucose.md` + `...-en.md`
  - emotion（2 组）：
    - `docs/blog/prevention/emotion/stress-eating-cravings-glucose.md` + `...-en.md`
    - `docs/blog/prevention/emotion/five-minute-calm-toolbox.md` + `...-en.md`
- 每篇文章包含：`lang` + `translation_key`、双语互链、至少一张 Wikimedia 图片与来源、内外链、以及文末 `{% include related-articles.html %}`。
- 更新四个分类索引页（中英各一）把新增文章挂出并可点击进入：
  - `docs/blog/prevention/diet/index.md` / `index-en.md`
  - `docs/blog/prevention/exercise/index.md` / `index-en.md`
  - `docs/blog/prevention/sleep/index.md` / `index-en.md`
  - `docs/blog/prevention/emotion/index.md` / `index-en.md`

### Next step
对全站做本地校验：grep 禁用词、核对 translation_key 成对、检查索引/互链是否漏 `.md` 或路径错误；发现问题即修复，并继续追加本日志。
