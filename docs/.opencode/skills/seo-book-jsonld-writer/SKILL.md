---
name: seo-book-jsonld-writer
description: Generate production-ready JSON-LD for book-related blog and landing pages based on Google-required fields and Schema.org Book enrichment.
version: 1.2.0
---

# SEO Book JSON-LD Writer

## Use this skill when
- A book blog post or ebook page is ready for schema implementation.
- You already have metadata (title, author, ISBN, format, etc.).

## Input checklist
- canonical URL
- page title and description
- publication or update date
- book metadata (name, author, isbn, format, pages)
- publisher/organization details
- author roster source (`docs/_book/batch-email.csv`)
- author identity fields (`author_id`, `author_email`, `author_role`)
- reviewer identity fields when applicable

## Output requirements
Return:
1. a JSON-LD script block
2. a field mapping table (`field -> source`)
3. a short missing-field report
4. a validator handoff note listing what must be checked before publish
5. recommended `author` / `reviewedBy` mapping notes for front matter and schema consistency

## Authority order
When choosing fields and types, use this priority:
1. Google Search Central requirements for the target rich result
2. Schema.org vocabulary needed to complete the entity cleanly
3. Project-specific enrichment only when it stays factual and user-visible

## Implementation rules
- Prefer Google-supported Book rich result properties first.
- Add Schema.org Book enrichment fields only when data exists.
- Use `@context: https://schema.org`.
- Keep JSON valid and minimal; avoid speculative placeholders.
- If a field is unknown, omit it and report it in missing-field report.
- Only include properties the page content, metadata, or trusted first-party source can prove.
- Keep JSON-LD as the default format; do not switch to Microdata or RDFa.
- Do not add `FAQPage` for normal commercial/book marketing pages.
- Do not add deprecated `HowTo` rich-result markup.
- Never fabricate ISBN, aggregate ratings, review counts, awards, or availability.
- Author identity in schema must match the page-visible byline metadata.
- If persona is editorial (non-licensed role), avoid implying protected professional credentials in schema.

## Persona roster mapping (for this project)
Use `docs/_book/batch-email.csv` as source of truth. Current roster:
- `zzh` / `zzh@tangyou.space` / 糖尿病治疗期病人
- `kelvin` / `kelvin@tangyou.space` / 糖尿病研究人员
- `yyh` / `yyh@tangyou.space` / 糖尿病治疗医生
- `gwx` / `gwx@tangyou.space` / 糖尿病康复期病人
- `zyn` / `zyn@tangyou.space` / 医学院学生
- `zhl` / `zhl@tangyou.space` / 糖尿病病人家属
- `wep` / `wep@tangyou.space` / 糖尿病病人家属

Preferred schema pattern:
- `author.name`: display name used on page
- `author.email`: roster email
- `author.description`: role text from roster
- `reviewedBy`: add for medically sensitive pages when reviewer exists

## Placement guidance
- Embed JSON-LD in page `<head>` or valid body script location.
- Keep content and schema consistent (same title, author, and description intent).
- Ensure key book facts used in schema also appear visibly on the page when feasible.

## Quality rules
- No fabricated ISBN, ratings, or review counts.
- No keyword stuffing in description fields.
- Ensure entity names are consistent across the site.

## Validation handoff
Before shipping, the next step must verify:
1. JSON parses cleanly.
2. Rich Results Test shows no blocking eligibility issues for the intended type.
3. Schema Markup Validator shows no invalid type/property combinations.
4. Any omitted fields are documented as missing data, not silently ignored.

## Success criteria
- JSON parses successfully.
- All Google-required properties for the selected type are present when available.
- Data matches page content and metadata.
- Every emitted field is traceable to a concrete source.
