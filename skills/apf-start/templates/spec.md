# SPEC-<NNN>: <Title>

Format: IEEE 29148-style requirements (what), RFC/design-doc design (how), MADR 4.0 decision record (why). The words MUST, SHOULD and MAY follow RFC 2119.

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
Verifiable, uniquely identified, design-independent. Each links to the PRD requirement it implements.

| ID | Requirement | Implements | Verification (test / inspection / analysis) |
|---|---|---|---|
| R-1 | The system MUST ... | PR-1 | |

### 4.1 Interfaces
External interfaces (APIs, config, wire formats, CLI).

### 4.2 Quality attributes
Performance, availability, security, compatibility, operability, each with a measurable target.

### 4.3 Constraints
Imposed design and environment constraints. The implementation MUST conform to `conventions.md` (project config, surrounding code, and technology idiom) and to the hard constraints in `product-guiding-principles.md` (cite the HC-n IDs that apply).

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
Reproducer (end-to-end) plus unit and integration coverage, each traceable to requirement IDs. Tests must be isolable per worktree (`conventions.md`, "Test isolation"): state any exclusive resource a test needs.

## 11. Operational hooks
Signals the SOP attaches to: metrics, logs, alerts, health checks, feature flags, rollback switches.

## 12. Decision record (MADR 4.0)

### Context and problem statement
### Decision drivers
### Considered options
(from the gate-1 option table, with pros and cons)
### Decision outcome
Chosen option, and why. Consequences (good, bad).
### Confirmation
How compliance with this decision will be confirmed.

## 13. Open questions

## 14. References
Every claim in this document cites a `file:line` or URL.
