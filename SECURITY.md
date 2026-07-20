# Security policy and threat model

## Reporting a vulnerability

Report vulnerabilities privately to [lliang@outlook.com](mailto:lliang@outlook.com). Include a concise impact summary, affected version or commit, reproduction conditions and a safe contact method. Do not include real credentials, private learner notes or unrelated personal data.

GitHub Private Vulnerability Reporting was checked through the repository API on 2026-07-20 and is currently disabled. The maintainer selected the security email above as the private reporting channel, so this repository does not claim that GitHub Private Vulnerability Reporting is enabled.

This educational project does not claim production isolation. The default labs are offline and do not execute arbitrary untrusted code.

## Supported surface

Security fixes target the current `main` branch and the latest published release candidate. Archived V1 files under `workbook/archive/legacy-v1/` are evidence only and are never executed or deployed.

## Threat model

| Asset | Trust boundary / attack path | Prevention | Detection | Recovery |
| --- | --- | --- | --- | --- |
| Tool names and arguments | Model output enters registry | Explicit registry, strict schema, deny unknown tools, approval for side effects | Unit and integration tests, trace stop reasons | Stop run; never broaden permissions automatically |
| Calculator input | Model/user expression reaches evaluator | Restricted AST and resource limits; no `eval`/`exec` | Security corpus and residual search | Return structured fatal error |
| File paths | Model/user path reaches filesystem | Resolve under an explicit base; separate read/write permissions | Path traversal tests | Deny without revealing host path |
| Database input | Values reach SQL | Bound parameters and fixed query shape | SQL-injection regression | Roll back and return redacted error |
| Demonstration code | Trusted lesson string reaches child process | Not exposed as a general tool; explicitly not a sandbox | Cross-platform timeout test | Terminate; optional container lab only |
| Search and retrieval content | Untrusted text enters context | Size limits, source metadata, claim-to-chunk validation | Fixed RAG eval set | Return insufficient evidence |
| Markdown and search input | Browser data reaches DOM | Locked parser plus DOMPurify, text fallback, CSP, no inline handlers | Vitest, Playwright and axe attacks | Preserve raw note locally; render safe text |
| Progress import | JSON replaces local state | Versioned schema, preview, backup and atomic replacement | Count reconciliation and rollback tests | Restore backup |
| API keys and errors | Environment/provider crosses model or log boundary | Environment-only keys and redacted errors | Secret scan and error tests | Revoke key; delete local state |
| Long-term memory | Learner content enters SQLite | Consent, minimization, TTL, secret rejection, delete/clear | Persistence, expiry and deletion tests | Delete/clear and verify no retrieval |
| Dependencies and Actions | npm/Python/Actions supply chain | Lock files, Dependabot, pinned Actions, no latest CDN | Audit workflows | Revert lock and rebuild known source |
| Pages deployment | Static artifact becomes public | Minimal permissions, environment gate, recorded source commit | Strict build and browser tests | Rebuild last verified source commit |

## Code-execution boundary

`stage-2/tools_safety.py::run_code_with_timeout_demo` runs only fixed trusted lesson strings. A timeout and Unix CPU limit do not isolate files, network, credentials, users or kernel resources. Optional arbitrary-code experiments must use ADR-0005 controls and report a skip when Docker/WSL is unavailable.

## Private data

Personal notes, exports and SQLite files stay local and are ignored by Git. Public fixtures use synthetic data. The project includes no analytics or remote synchronization.
