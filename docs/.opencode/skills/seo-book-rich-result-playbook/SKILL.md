---
name: seo-book-rich-result-playbook
description: Turn book-related topics into rich-result-ready page briefs with schema goals, content requirements, and CTR-oriented SERP presentation.
version: 1.2.0
---

# SEO Book Rich Result Playbook

## Use this skill when
- Choosing which book topics/pages to produce next.
- You want each page brief to be both content-strong and schema-ready.

## Page brief template
For each target page, define:
1. target query and search intent
2. page purpose (review, summary, recommendation, landing)
3. target rich result appearance
4. required on-page evidence for schema fields
5. JSON-LD field pack (required/recommended/enrichment)
6. CTA path (newsletter, ebook download, independent-site action)
7. validator plan (Rich Results Test, Schema Markup Validator, or both)
8. byline plan (`author_id`, `author_role`, optional `reviewer_id`)
9. disclaimer plan (`medical-information-only` or stricter key)

## Source and decision hierarchy
Use this order:
1. Choose the intended Google search appearance first.
2. Derive required/recommended fields from Google guidance.
3. Add Schema.org Book enrichment only when it improves clarity.
4. Confirm each field can be supported by visible page content or trusted first-party metadata.

## Writing + schema coordination
- Only include schema properties that the page actually proves.
- Align headline, metadata, and JSON-LD entities.
- Ensure book facts (author, isbn, format, page count) are visible to users, not only hidden in schema.
- If a key field is missing, turn it into a content requirement rather than a guessed schema value.
- Keep byline metadata, author profile text, and schema `author` entity consistent.

## SERP presentation goals
- Improve eligibility for rich display.
- Improve snippet clarity and trust signals.
- Increase CTR with precise factual metadata.
- Prefer one primary rich-result goal per page unless the page naturally supports more than one.

## Monetization coordination
- Keep conversion CTAs separate from factual schema claims.
- Use schema to improve discovery; use content blocks to monetize.
- For health-adjacent book content, preserve safety disclaimers and trust tone.

## Shared structured-data rules
- Use JSON-LD by default.
- Do not recommend deprecated `HowTo` rich-result strategies.
- Do not recommend `FAQPage` for standard commercial/book marketing pages unless the site clearly qualifies under current restrictions.
- Use current page-experience language (`INP`, not `FID`) in SEO rationale.
- Never use fake ratings, review counts, or placeholder entity data to chase richer SERP presentation.

## Pre-publish release gate
Before a brief is considered implementation-ready, it must specify:
1. the exact schema type target
2. the visible evidence required for each critical field
3. which validator(s) will be used
4. what blocks release versus what can ship with caution
5. which persona writes and who reviews medically sensitive content

## Maintenance cadence
- Revisit rich-result targets when Google changes documentation or supported types.
- If source guidance is older than 90 days, verify it before reusing the brief unchanged.

## Success criteria
- Each brief can be executed by content + technical SEO without missing data.
- Rich result target is explicit and testable.
- CTA design is included without polluting schema quality.
- Required fields and validation path are fully specified before writing JSON-LD.
