---
title: "{{TITLE}}"
date: {{PUBLISH_DATETIME_ISO8601}}
description: "{{META_DESCRIPTION}}"
categories: ["{{CATEGORY_PRIMARY}}"]
tags: ["{{TAG_1}}", "{{TAG_2}}", "{{TAG_3}}"]
slug: "{{SLUG}}"

# Persona fields (auto-fill from docs/_book/author-role-rotation.csv)
author_id: "{{AUTHOR_ID}}"
author_name: "{{AUTHOR_NAME}}"
author_email: "{{AUTHOR_EMAIL}}"
author_role: "{{AUTHOR_ROLE}}"

# Review fields
reviewer_id: "{{REVIEWER_ID}}"
reviewer_name: "{{REVIEWER_NAME}}"
reviewer_email: "{{REVIEWER_EMAIL}}"
reviewer_role: "{{REVIEWER_ROLE}}"
review_status: "draft" # draft|reviewed|published
reviewed_at: "{{REVIEWED_AT_ISO8601_OR_EMPTY}}"

# Compliance/disclaimer routing
disclaimer_key: "medical-information-only"

# Funnel mapping
ebook_id: "{{EBOOK_ID}}"
download_url: "{{DOWNLOAD_URL}}"
cta_form_id: "{{CTA_FORM_ID}}"
automation_id: "{{AUTOMATION_ID}}"
---

## How to auto-fill from rotation table

Source: `docs/_book/author-role-rotation.csv`

1. Determine `day_index` from publish date in Asia/Shanghai timezone.
2. Pick the matching row in the CSV (`1..7`).
3. Fill `author_*` and `reviewer_*` fields from that row.
4. Keep `review_status=draft` before review, then update to `reviewed`/`published`.

### Deterministic weekly cycle rule

- If using calendar weekday mapping: Monday=1 ... Sunday=7.
- If using rolling index mapping: `day_index = ((N - 1) % 7) + 1`, where `N` is days since a fixed start date.

## Minimal front matter variant

```yaml
---
title: "{{TITLE}}"
date: {{PUBLISH_DATETIME_ISO8601}}
author_id: "{{AUTHOR_ID}}"
author_email: "{{AUTHOR_EMAIL}}"
author_role: "{{AUTHOR_ROLE}}"
reviewer_id: "{{REVIEWER_ID}}"
review_status: "draft"
disclaimer_key: "medical-information-only"
---
```
