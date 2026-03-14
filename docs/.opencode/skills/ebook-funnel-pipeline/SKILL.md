---
name: ebook-funnel-pipeline
description: Orchestrate the full ebook-to-blog-to-upload-to-email funnel using the repo's local skills and operational constraints.
version: 1.2.0
---

# Ebook Funnel Pipeline

## Use this skill when
- You want to run the entire daily ebook funnel from intake to delivery.
- You need one repeatable checklist that coordinates all downstream skills.

## Hard execution constraints (project policy)
- Markdown-only output for blog generation tasks (`*.md` files only).
- Do NOT run `bundle` commands (`bundle exec jekyll build|serve` etc.) during blog-generation execution.
- Do NOT run git commit/push/amend/rebase as part of blog-generation execution.
- If verification is needed, use content-level checks (front matter completeness, path/index sync, URL checks), not site builds.

## Daily output quota (mandatory)
- Generate **10 Chinese posts + 10 corresponding English posts** every publishing day.
- "Corresponding" means each ZH post has a paired EN post with the same `translation_key` and matched slug family (`slug` / `slug-en`).
- If one bilingual pair is already produced, continue generating the remaining pairs in the same day until the daily total reaches 10 pairs.

## Article quality floor (mandatory)
- Chinese article length target: **1500-2000 Chinese characters per post**.
- English article length target remains long-form and must not be a stub or outline-only draft.
- Prefer image-rich presentation: add **2 or more relevant images** when suitable, using stable external URLs with clear alt text.
- Images should support comprehension (meal structure, monitoring tools, grocery planning, walking, kitchen workflow), not act as decorative filler.

## Pipeline order
1. `ebook-asset-intake`
2. `ebook-funnel-monetization`
3. `ebook-funnel-blog-writer`
4. `ebook-server-publisher`
5. `ebook-email-delivery`

## Daily operating procedure
1. Scan `/media/danezhang/Elements/seo/blog/ebook` for the new batch.
2. Build a dated manifest in `/media/danezhang/Elements/seo/blog/workdir`.
3. Select the best ebooks for traffic and monetization potential.
4. Select the daily persona using `docs/_book/author-role-rotation.csv`.
5. Classify each selected topic into `stage x dimension` taxonomy (`prevention|treatment|rehabilitation` x `exercise|diet|emotion|sleep`).
6. Generate one or more funnel blog drafts from the selected ebooks.
7. Enforce long-form length gate before publish:
   - ZH target: 1500–2000 Chinese characters
   - EN target: 1200–1800 words
   - if below range, expand content before continuing
8. Write files to canonical paths only:
   - `docs/blog/{stage}/{dimension}/{slug}.md`
   - `docs/blog/{stage}/{dimension}/{slug}-en.md`
9. Sync entry links in root/stage/dimension index pages.
6. Upload the final ebook assets to `https://download.tangyou.space/yyyyMMdd/filename`.
7. Bind each blog CTA to the correct ebook identifier and download URL.
8. Insert or update the email subscription entry point in the corresponding blog post.
9. Trigger the correct automated delivery email.
10. Record publish log: date, slug, author persona, reviewer persona, disclaimer key.

## Mandatory taxonomy and indexing policy
- Stage values: `prevention | treatment | rehabilitation`
- Dimension values: `exercise | diet | emotion | sleep`
- For each new bilingual pair, update all three index layers:
  - `docs/blog/index*.md`
  - `docs/blog/{stage}/index*.md`
  - `docs/blog/{stage}/{dimension}/index*.md`
- Remove obsolete top-level duplicates after migration.

## Required records per ebook
- sanitized filename
- public download URL
- target blog slug
- target search intent
- monetization path
- email form identifier
- email automation identifier
- author_id
- author_email
- author_role
- reviewer_id (required for high-risk medical topics)
- disclaimer_key

## Canonical persona scheduling files
- Roster source: `docs/_book/batch-email.csv`
- Rotation source: `docs/_book/author-role-rotation.csv`
- Front matter template source: `docs/_book/templates/jekyll-front-matter-persona.md`

## Rotation execution rule
- Use `day_index` from `author-role-rotation.csv` to resolve `author_*` and `reviewer_*`.
- Weekly mapping default: Monday=1 ... Sunday=7 (Asia/Shanghai).
- Do not override row order unless roster changes are approved and rotation table is regenerated.

## Decision rules
- If the ebook quality or topic is weak, skip it rather than publishing low-trust content.
- If filename cleanup is ambiguous, preserve meaning and log the transformation.
- If an ebook is strong for SEO but weak for affiliate monetization, use ads plus independent-site CTA instead.
- If a blog post is highly transactional, reduce ad density and prioritize the independent-site CTA.
- If today uses `yyh` or `kelvin` as author, prioritize educational framing and source-backed claims.
- If today uses patient/family personas (`zzh`, `gwx`, `zhl`, `wep`), keep medical advice language conservative and ensure reviewer is `yyh` or `kelvin` for sensitive sections.

## Success criteria
- Every selected ebook has a sanitized server URL.
- Every generated blog has a mapped ebook CTA.
- Every subscriber receives the matching download link.
- Every asset has a clear primary monetization path.
