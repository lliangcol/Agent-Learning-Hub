# Security regression scope

Permanent gates cover restricted calculator input, path traversal, SQL binding, tool permission denial, error redaction, browser injection, progress import atomicity, and SQLite consent/expiry/deletion.

The browser corpus includes script elements, event attributes, `javascript:` URLs, SVG payloads, Markdown raw HTML and malicious search text.
