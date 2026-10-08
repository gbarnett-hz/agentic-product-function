---
name: product-foundations
description: One-time interactive setup that creates a project's product-vision.md, product-guiding-principles.md and company-context.md with the user, then references them from AGENTS.md. Run it once, before /agentic-product-function or /create-prd. Use when the user says "product-foundations", "set up the product vision", "write our guiding principles", "set up company context", or is starting a new project for the agentic team and has none of these files.
---

# product-foundations

You help the human write the three documents every agent in the team is grounded in. Run once per project, before `/agentic-product-function` and `/create-prd`. Re-running refines existing files; it never silently overwrites them.

| File (project root) | What it holds | Template |
|---|---|---|
| `product-vision.md` | The end goal: what we are building, for whom, and why | `templates/product-vision.md` |
| `product-guiding-principles.md` | The fundamentals the project adheres to (hard constraints like "Java 21", "zero runtime memory allocation", plus judgement principles) | `templates/product-guiding-principles.md` |
| `company-context.md` | The company's execution space and guiding philosophies | `templates/company-context.md` |

`<skill dir>` is the folder containing this SKILL.md. Use the templates exactly; do not add or drop sections. Project files are relative to the user's project root.

## 1. Orient
- Check which of the three files exist. If one exists, read it and offer to refine it (show a diff before writing); never replace it wholesale.
- Skim what the repo already says so you ask only what it does not answer: `README`, `CLAUDE.md`, `AGENTS.md`, build files (`pom.xml`, `build.gradle`, `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`), CI config, `docs/`.
- Facts you infer (for example Java 21 from a build file) are **suggestions**: put them to the user to confirm. Never write an inferred fact as decided.
- Ask which document to start with. Default order: vision, principles, company context. The user may skip or reorder.

## 2. Interview, one document at a time
Ask in small batches (`AskUserQuestion` for choices, plain questions for open answers), only for what is missing. Do not invent facts, metrics, customers or company details: unknown goes under Open questions.

**Vision** — cover: the vision in one sentence; who it is for; the problem or need; what the product is, and what it will never be; what makes it different; how success is measured; the rough horizon (now / next / later). Push back on vague or purely aspirational statements ("best-in-class", "seamless") and ask what would be true in the world if it succeeded.

**Guiding principles** — cover: hard constraints first (language and runtime versions, memory/allocation, latency, compatibility, licensing, dependency policy, supported platforms), then the principles that guide judgement calls. For every one:
- State it as an imperative, testable sentence.
- Give the rationale (why we hold it).
- Give the implications (what it forces and what it forbids).
- Give the verification: how a reviewer or tool checks it (a lint rule, a benchmark, a test, a review checklist). If it can only be judged, mark it `judgement`.
- Name who may grant an exception, and how.
Push back on principles that cannot be checked or that contradict each other, and ask which wins when they conflict (record an explicit priority order).

**Company context** — cover: what the company does and its market; customers and segments; strategy and current priorities; how the company makes decisions and what it values; execution constraints (team shape, release cadence, compliance and security requirements, hosting and deployment norms, support model, approved or forbidden vendors and technologies); terms used internally.

## 3. Draft, review, write
1. Write the draft to `drafts/<file>.md` (create `drafts/` if missing). Show it and edit it in place for requested changes.
2. Only when the user approves, write it to the project root as `<file>.md` in a single write and delete the draft.
3. Move on to the next document.

## 4. Reference them from AGENTS.md
After each file is written, update the managed block in `AGENTS.md` at the project root so it lists exactly the foundation files that exist. If `AGENTS.md` is missing, create it containing only the block. Replace what is between the markers; never touch anything outside them.

```markdown
<!-- product-foundations:start -->
## Product foundations
Read these before planning, designing or writing code. They are the source of truth for what we build and the constraints we hold.
- [product-vision.md](product-vision.md): the end goal, who it is for, and how success is measured.
- [product-guiding-principles.md](product-guiding-principles.md): the fundamentals every change must adhere to. Hard constraints are MUST-level and verified.
- [company-context.md](company-context.md): the company's execution space and guiding philosophies.

If a request conflicts with a hard constraint in the guiding principles, stop and raise it instead of working around it.
<!-- product-foundations:end -->
```
(List only the files that exist.)

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. Check for `CLAUDE.md`:
- Missing: create it containing `@AGENTS.md`.
- Present without an `@AGENTS.md` import: show the one line you would add and ask before adding it.
- Already imports it: nothing to do.

## 5. Finish
Tell the user which files were written, that `AGENTS.md` now references them, and the next steps: `/agentic-product-function lanes=N`, then `/create-prd`. Suggest committing the files.
