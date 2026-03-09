---
name: seo-schema-validation-loop
description: Validate and harden structured data with Rich Results Test and Schema Markup Validator, then ship a fix list for ranking-safe deployment.
version: 1.1.0
---

# SEO Schema Validation Loop

## Use this skill when
- JSON-LD has been generated and embedded.
- You want a pre-publish QA gate for schema correctness.

## Validation stack
1. Google Rich Results Test (eligibility + rich result issues)
2. Schema Markup Validator (syntax + vocabulary correctness)

## Validation principles
- Treat Google support as the primary release gate for rich-result intent.
- Treat Schema.org validation as the vocabulary and syntax backstop.
- Validate only claims the page can support with visible or trusted first-party data.
- If a field is missing, remove it or mark it for content completion; do not fake it.

## QA workflow
1. Run both validators for target page(s).
2. Capture errors, warnings, and unsupported properties.
3. Prioritize fixes in this order:
   - syntax/parsing errors
   - missing required properties
   - invalid type/property pairs
   - quality warnings
4. Re-run validators until no blocking issues remain.
5. Archive the final validator status with the page URL and tested schema type.

## Required output
- validation summary (pass/fail)
- issue list grouped by severity
- exact fix actions
- re-test result status
- release decision (`block`, `caution`, `pass`)

## Severity policy
- Block release: parsing errors, missing required fields, invalid property types
- Can release with caution: non-critical warnings with mitigation notes

## Shared structured-data rules to enforce
- JSON-LD is the default and preferred implementation format.
- Do not approve deprecated `HowTo` rich-result implementations.
- Do not approve `FAQPage` for normal commercial/book landing use unless the site clearly meets Google's restricted use cases.
- Reject any schema that still references outdated CWV language such as `FID` where current guidance should use `INP`.
- Reject unsupported properties added only to make the markup look larger.

## Anti-patterns to avoid
- Shipping schema with known parsing errors
- Adding unsupported properties only to inflate schema size
- Claiming rich result eligibility without validator evidence
- Keeping fields that cannot be tied back to page content or first-party metadata

## Maintenance cadence
- Re-check validation guidance after major Google structured-data documentation updates.
- Flag any saved validation checklist older than 90 days for a quick re-review.

## Success criteria
- No blocking issues.
- Validator output is archived in deployment notes.
- Schema changes are traceable to actual content data.
- Release status is explicit and evidence-backed.
