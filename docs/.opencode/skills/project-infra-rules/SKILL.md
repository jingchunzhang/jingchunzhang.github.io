# Project Infrastructure Rules

This skill defines the mandatory infrastructure rules for the project.

## Dependency Management

**CRITICAL RULE:** Do NOT store executable programs or node dependencies (like `node_modules`) directly in the project root.

**Target Location:** All dependencies and executables must reside in:
`/home/danezhang/dev/blog/depends`

### Implementation for Node.js
1.  Move `node_modules` to `/home/danezhang/dev/blog/depends/node_modules_docs` (or appropriate subfolder).
2.  Create a symlink in the project root pointing to the external location:
    ```bash
    ln -s /home/danezhang/dev/blog/depends/node_modules_docs node_modules
    ```

### Rationale
To keep the project directory clean and manage dependencies in a centralized location outside the source tree.
