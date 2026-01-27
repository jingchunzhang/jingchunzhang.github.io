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
