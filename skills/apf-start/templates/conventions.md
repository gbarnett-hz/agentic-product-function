# Conventions

Project-level, written by ACore and refreshed when the stack changes. Developers follow it, testers check it, the integrator and Verifier enforce it.

**Authority order** (higher wins):
1. The project's own enforced configuration (formatter, linter, type checker, CI, `CLAUDE.md`, `CONTRIBUTING`).
2. The patterns already in the code being touched.
3. The technology's official or community idiom (cite it).

Repeat the block below once per technology in the project.

## <Technology, e.g. Java 21 / Python 3.12 / Go 1.23 / Terraform>

- **Where it is used:** paths.
- **Idiom standard(s):** name and URL (e.g. PEP 8, Effective Go, Google Java Style Guide, Rust API Guidelines).
- **Mechanical checks (run before handoff, all must pass):**

  | Check | Command | Source (config file or doc) |
  |---|---|---|
  | Format | | |
  | Lint | | |
  | Types / static analysis | | |
  | Tests | | |

- **Project-specific rules** (from config, CLAUDE.md, CONTRIBUTING, review history): naming, error handling, logging, concurrency, dependency policy, test layout, commit/PR rules.
- **Patterns to copy:** `path/file:line` examples of the idiom in this codebase.
- **Where project and general idiom differ:** which one wins and why.
- **Gaps:** checks that do not exist (e.g. no linter configured), so reviewers cover them by hand.
