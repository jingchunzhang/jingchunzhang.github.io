---
name: ebook-server-publisher
description: Upload sanitized ebook files to the download server, keep deterministic dated URLs, and return the final public link for each asset.
version: 1.0.0
---

# Ebook Server Publisher

## Use this skill when
- An ebook file has already been selected and its destination filename has been sanitized.
- You need to publish the file to the download server and produce a public URL.

## Infrastructure constraints
- Upload protocol: `scp`
- Remote host: `ubuntu@167.148.165.189`
- Remote root: `/var/www/html/download.tangyou.space/yyyymmdd/`
- Public URL pattern: `https://download.tangyou.space/yyyymmdd/filename`
- `yyyymmdd` example: `20260308`

## Filename constraints
- Replace spaces with `-`.
- Remove original basename content inside trailing parentheses or everything after the first `(` / `（` in the basename before the extension.
- Preserve the file extension.
- Use the sanitized basename as the public URL basename.

## Workflow
1. Confirm the source file exists locally.
2. Derive `yyyymmdd` from the publish date.
3. Generate the sanitized basename.
4. Ensure the remote date directory exists before upload.
5. Upload the file via `scp`.
6. Return the final HTTPS download URL.
7. Record the mapping in the manifest used by blog and email automation.

## Required verification
- Confirm the uploaded file path matches the sanitized basename.
- Confirm the returned URL uses the same basename.
- Avoid silent renames after upload.

## Output format
Return a compact deployment record:
- `source_path`
- `upload_date`
- `remote_path`
- `public_url`
- `final_basename`
- `status`

## Failure handling
- If the remote directory is missing, create it first.
- If upload fails, report the exact file and exact failing command.
- Do not claim success without a final URL.
