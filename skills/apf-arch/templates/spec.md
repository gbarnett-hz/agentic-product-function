# SPEC-<NNN>: <Title>

Format: given-when-then behavioural requirements (what, derived from the PRD) approved before any code analysis; then RFC/design-doc design (how) and a MADR 4.0 decision record (why), completed after the option is chosen. The words MUST, SHOULD and MAY follow RFC 2119.

| | |
|---|---|
| Status | Draft / Approved |
| Author | AExpert |
| PRD | <link to prds/PRD-NNN.md> |
| Date | <YYYY-MM-DD> |
| Supersedes | <SPEC-NNN or none> |

## 1. Summary
What this spec delivers, in a paragraph.

## 2. Motivation
Why. Distilled from the PRD problem statement, with the evidence that grounds it (cite sources).

## 3. Goals and non-goals
- **Goals:**
- **Non-goals:**

## 4. Requirements (what)
Every PRD requirement becomes one or more behavioural scenarios in Given/When/Then form. Design-independent: no implementation, technology or file paths. Each scenario is uniquely identified, links to the PRD requirement it implements, and is the acceptance criterion the Verifier checks later.

| ID | Given | When | Then | Implements |
|---|---|---|---|---|
| R-1 | a client sends requests to the public API | the client exceeds the allowed rate | the API MUST reject the request with HTTP 429 and a Retry-After header | PR-1 |

### 4.1 Interfaces
External interfaces (APIs, config, wire formats, CLI).

### 4.2 Quality attributes
Performance, availability, security, compatibility, operability, each with a measurable target.

### 4.3 Constraints
Imposed design and environment constraints. The implementation MUST conform to `conventions.md` (project config, surrounding code, and technology idiom) and to the hard constraints in `product-guiding-principles.md` (cite the HC-n IDs that apply).

> Sections 5-12 are written **after** the analysis and your option choice (gate 2), with no further approval. A change to an approved scenario in section 4 does need re-approval of the delta.

## 5. Design (how)
Architecture and key mechanisms, with `path/to/file:line` references to the existing code. Include data flow and failure behaviour.

## 6. Cloud impact
Side effects on cloud deployment (from ACloud).

## 7. Enterprise impact
Fit with enterprise deployments and existing services (from ASolution).

## 8. Compatibility and upgrade
Rolling upgrade, wire/serialization compatibility, migration, deprecation.

## 9. Risks and mitigations
| Risk | Likelihood | Impact | Mitigation | Requirement IDs |
|---|---|---|---|---|

## 10. Test strategy and acceptance criteria
Reproducer (end-to-end) plus unit and integration coverage, each traceable to the scenario IDs. Tests must be isolable per worktree (`conventions.md`, "Test isolation"): state any exclusive resource a test needs.

## 11. Operational hooks
Signals the SOP attaches to: metrics, logs, alerts, health checks, feature flags, rollback switches.

## 12. Decision record (MADR 4.0)

### Context and problem statement
### Decision drivers
### Considered options
(from the gate-2 option table, with pros and cons)
### Decision outcome
Chosen option, and why. Consequences (good, bad).
### Confirmation
How compliance with this decision will be confirmed.

## 13. Open questions

## 14. References
Every claim in this document cites a `file:line` or URL.
