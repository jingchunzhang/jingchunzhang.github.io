---
name: ebook-funnel-blog-writer
description: Generate lead-generation blog posts from ebook content and connect them to ads, affiliate offers, and the independent site without breaking YMYL trust.
version: 1.2.0
---

# Ebook Funnel Blog Writer

## Use this skill when
- You already have an ebook manifest or extracted content.
- You want to publish a blog post that brings search traffic and converts readers into subscribers or buyers.
- You need a post that supports three monetization paths: Google ads, independent site, and affiliate links.

## Hard execution constraints (project policy)
- Output scope is Markdown content only (`*.md` blog and index updates).
- Do NOT run `bundle` or any Jekyll build/serve command while executing this skill.
- Do NOT run git commit/push/amend/rebase while executing this skill.
- Completion is defined by md file generation/update quality and index synchronization, not by build execution.

## Primary goal
Turn one ebook into one high-intent funnel article that:
- ranks for a specific long-tail search intent
- offers a relevant ebook as the lead magnet
- naturally routes readers to monetization assets

## Author persona roster (from `docs/_book/batch-email.csv`)
Use these role identities for bylines and narrative perspective:
- `zzh` (`zzh@tangyou.space`) — 糖尿病治疗期病人
- `kelvin` (`kelvin@tangyou.space`) — 糖尿病研究人员
- `yyh` (`yyh@tangyou.space`) — 糖尿病治疗医生
- `gwx` (`gwx@tangyou.space`) — 糖尿病康复期病人
- `zyn` (`zyn@tangyou.space`) — 医学院学生
- `zhl` (`zhl@tangyou.space`) — 糖尿病病人家属
- `wep` (`wep@tangyou.space`) — 糖尿病病人家属

## Daily role rotation rule
- Rotate one primary persona per post day.
- Avoid using the same primary persona on consecutive publishing days.
- If a post is highly medical, set `yyh` (医生) or `kelvin` (研究人员) as reviewer even if not primary author.
- Keep a short publish log: `date -> slug -> primary persona -> reviewer persona`.

## Canonical rotation table (auto-read)
- Primary file: `docs/_book/author-role-rotation.csv`
- Columns: `day_index, author_id, author_email, author_role, reviewer_id, reviewer_email, reviewer_role, rule_note`
- Daily mapping rule:
  - weekly mode: Monday=1 ... Sunday=7
  - rolling mode: `day_index = ((N - 1) % 7) + 1`
- If a day has multiple posts, keep the same primary persona but allow reviewer changes by risk level.

## Blog requirements
- Match the repo's Jekyll Markdown style and front matter.
- Prefer clear, citation-ready structure for AI search and Bing-style answer extraction.
- Use a strong Title, Description, H2/H3 structure, FAQ, and internal links.
- Add a clear ebook CTA in the middle and near the end of the article.
- Leave room for Google ads in high-visibility but non-disruptive sections.
- Add affiliate recommendations only when contextually relevant.
- Add an independent-site CTA for the deeper solution, toolkit, or paid offer.

## Mandatory classification taxonomy (for diabetes funnel posts)
- Every new post MUST be classified into a 2-level path:
  1) Stage: `prevention | treatment | rehabilitation`
  2) Dimension: `exercise | diet | emotion | sleep`
- Final path format MUST be:
  - `docs/blog/{stage}/{dimension}/{slug}.md` (ZH)
  - `docs/blog/{stage}/{dimension}/{slug}-en.md` (EN)
- Do not keep duplicate top-level copies under `docs/blog/{slug}.md` once migrated.
- Index sync is mandatory for each published pair:
  - `docs/blog/index.md` and `docs/blog/index-en.md`
  - `docs/blog/{stage}/index.md` and `docs/blog/{stage}/index-en.md`
  - `docs/blog/{stage}/{dimension}/index.md` and `docs/blog/{stage}/{dimension}/index-en.md`

## Mandatory content length range
- Chinese (ZH) long-form target: **1500–2000 Chinese characters** per post.
- English (EN) long-form target: **1200–1800 words** per post.
- If the first draft is below target, expand with practical sections (framework, checklist, FAQ, scenarios, cautions) before marking complete.
- Keep medical tone conservative: no cure claims, no absolute guarantees.

## Required front matter fields for persona publishing
- `author_id`: one of `zzh|kelvin|yyh|gwx|zyn|zhl|wep`
- `author_name`: display name (can be `zzh`, `kelvin`, etc.)
- `author_email`: must match roster email exactly
- `author_role`: role text from roster
- `reviewer_id`: optional but required for high-risk medical claims
- `review_status`: `draft|reviewed|published`
- `disclaimer_key`: e.g. `medical-information-only`

## Front matter template (auto-read)
- Use `docs/_book/templates/jekyll-front-matter-persona.md` as the canonical generation template.
- Always resolve `author_*` and `reviewer_*` from `docs/_book/author-role-rotation.csv` before draft output.

## Recommended article structure
1. Search-intent title focused on one reader problem.
2. Fast answer / key takeaways.
3. Main teaching section distilled from the ebook.
4. Practical checklist or framework.
5. FAQ block.
6. Mid-article ebook opt-in CTA.
7. Affiliate or tools block when relevant.
8. End-of-article CTA to:
   - subscribe for the ebook download
   - visit the independent site
   - explore related internal articles

## Monetization mapping
- **Google Ads**: favor informational queries with broad traffic and helpful content depth.
- **Independent site**: push readers to a product page, consultation page, or resource hub when intent becomes transactional.
- **Affiliate links**: recommend only adjacent tools/products genuinely aligned with the article topic.

## Safety and trust rules
- For health-related content, avoid cure claims and include a doctor-consult disclaimer where appropriate.
- Separate ebook-derived opinion from verified facts.
- Do not copy large passages verbatim from the ebook.
- Create original synthesis, summary, and reader-oriented structure.
- Do not claim real-world hospital affiliation, license number, or credential unless verifiable and approved.
- If using role-based personas, disclose editorial-role nature on author page and/or footer disclaimer.

## Deliverables
- Final Markdown article draft
- Suggested path/slug
- SEO title and meta description
- CTA copy for email signup
- Suggested internal links
- Suggested affiliate anchor text and independent-site anchor text
- Filled persona metadata (`author_id`, `author_email`, `author_role`, reviewer if needed)
