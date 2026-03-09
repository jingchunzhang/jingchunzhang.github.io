---
name: ebook-funnel-pipeline
description: Orchestrate the full ebook-to-blog-to-upload-to-email funnel using the repo's local skills and operational constraints.
version: 1.2.0
---

# Ebook Funnel Pipeline

## Use this skill when
- You want to run the entire daily ebook funnel from intake to delivery.
- You need one repeatable checklist that coordinates all downstream skills.

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
5. Generate one or more funnel blog drafts from the selected ebooks.
6. Upload the final ebook assets to `https://download.tangyou.space/yyyyMMdd/filename`.
7. Bind each blog CTA to the correct ebook identifier and download URL.
8. Insert or update the email subscription entry point in the corresponding blog post.
9. Trigger the correct automated delivery email.
10. Record publish log: date, slug, author persona, reviewer persona, disclaimer key.

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
