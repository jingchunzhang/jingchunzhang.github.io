---
name: ebook-asset-intake
description: Batch-process daily PDF/EPUB drops, normalize filenames, extract usable metadata, and prepare a manifest for upload and blog generation.
version: 1.0.0
---

# Ebook Asset Intake

## Use this skill when
- A new batch of ebooks is added to `/media/danezhang/Elements/seo/blog/ebook`.
- You need to prepare source files for upload, content extraction, or blog generation.
- You need a deterministic filename and metadata manifest before downstream automation.

## Hard constraints
- Source ebook directory: `/media/danezhang/Elements/seo/blog/ebook`
- Working directory: `/media/danezhang/Elements/seo/blog/workdir`
- Available conversion tool: `ebook-convert`
- Keep the original extension (`.pdf`, `.epub`, etc.).
- Replace spaces in the destination filename with `-`.
- Remove any basename content starting from `(` or `（` up to the matching closing bracket before the extension.
- Do not remove the extension.
- Never overwrite source files.

## Required output
Produce a batch manifest table with at least:
- `source_path`
- `source_basename`
- `sanitized_basename`
- `file_ext`
- `title`
- `author`
- `language` (best effort)
- `topic`
- `summary`
- `recommended_slug`

## Workflow
1. Scan the ebook source directory and identify the newly added files to process.
2. Create a dated work subdirectory under `/media/danezhang/Elements/seo/blog/workdir`.
3. Sanitize each filename:
   - remove bracketed suffixes such as `Book Name (z-lib.org).pdf`
   - replace spaces with hyphens
   - preserve the file extension
4. Extract metadata from the ebook if available.
5. If content extraction is needed, use `ebook-convert` to create a readable intermediate format in the workdir.
6. Generate a short factual summary and identify the monetizable angle:
   - Google ad-friendly informational angle
   - independent-site offer angle
   - affiliate recommendation angle
7. Save a manifest that downstream upload, blog, and email tasks can consume.

## Quality rules
- Prefer factual metadata over invented metadata.
- Flag low-confidence title/author extraction instead of guessing.
- Treat medical claims carefully; do not rewrite the ebook into unsafe health advice.
- If the ebook topic is unrelated to the current funnel, label it for manual review.

## Handoff to next skills
- `ebook-server-publisher` uses `sanitized_basename` and the dated manifest.
- `ebook-funnel-blog-writer` uses `title`, `topic`, `summary`, and monetization angle.
- `ebook-email-delivery` uses the final download URL plus ebook identity.
