---
name: seo-book-schema-strategy
description: Build a book-blog SEO schema plan using a goal-first method: Google supported rich results first, then Schema.org semantic enrichment.
version: 1.1.0
---

# SEO Book Schema Strategy

## Use this skill when
- You are planning SEO for book-related blog posts, review pages, or ebook landing pages.
- You want richer SERP presentation using structured data.
- You need a clear schema field strategy before writing JSON-LD.

## Core principle (from `ref_sub.md`)
Use reverse engineering, not field hoarding:
1. Start from the target Google rich result outcome.
2. Collect required/recommended fields from Google Search Central.
3. Enrich with high-value semantic fields from Schema.org Book vocabulary.
4. Implement JSON-LD and validate before publishing.

## Authoritative sources (the only default sources)
1. Schema.org
2. Google Search Central structured data docs
3. Google Rich Results Test + Schema Markup Validator

## Source hierarchy and planning order
Use this order every time:
1. Pick the target Google rich result or SERP presentation first.
2. Pull required and recommended properties from Google documentation.
3. Add Schema.org Book enrichment only when it improves entity clarity.
4. Map every property to a visible page source before approving implementation.
5. Mark anything unknown as missing instead of guessing.

## Planning output (required)
For each page, return:
- page type and intent
- target rich result type
- required properties (Google)
- recommended properties (Google)
- semantic enrichment properties (Schema.org Book)
- data source for each property
- visible on-page evidence required for each property
- validator target (`Rich Results Test`, `Schema Markup Validator`, or both)
- risk flags for missing fields

## Book-focused enrichment examples
- `bookFormat`
- `numberOfPages`
- `isbn`
- `author` entity details
- optional authoritative profile linkage for entities when available

## Constraints
- Use JSON-LD as the default format.
- Do not include fields with unknown values unless explicitly marked as missing.
- Avoid fake ratings/reviews.
- Prefer one clear rich-result target per page unless the page naturally supports more.
- Only plan properties the page can prove with visible content or trusted first-party metadata.

## Hard rules from shared SEO skills
- Google-supported rich result fields come before Schema.org expansion.
- Use `<script type="application/ld+json">`; do not plan Microdata or RDFa by default.
- `FAQPage` is restricted; do not treat it as a normal commercial-site recommendation.
- `HowTo` rich results are deprecated; do not plan for them.
- Use `INP`, not `FID`, when discussing page experience guidance.
- Keep monetization blocks, CTAs, and promotional copy separate from factual schema claims.

## Maintenance cadence
- Re-check this strategy when Google updates structured data guidance.
- Review assumptions if source references are older than 90 days.
- If a property has no stable source, leave it out of the plan and surface it as a content requirement.

## Success criteria
- Every schema plan traces each property to a known data source.
- Required properties are complete or explicitly marked missing.
- Enrichment fields increase entity clarity without introducing fabricated data.
