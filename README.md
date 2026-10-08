# agentic-product-function

A skill that models a product function as a team of agents. See `agentic-team.png` for the diagram.

**Status:** design in progress. Architecture function agreed; EM / engineering function TBD. Nothing is built yet.

## Players

| Agent | Role |
|---|---|
| **YOU** | Human in the loop. Writes PRDs, makes every approval decision. |
| **EM** (engineering-manager) | Watches the PRD directory, asks architecture for an assessment, allocates the plan to dev/test agents by capacity. *(TBD)* |
| **AExpert** (architect-chief) | Manages the architecture team and has the final word on output to you. Runs adversarial review, writes the spec, runs action-plan. The only agent that talks to you. |
| **ACore** (architect-core) | `deep-code` to understand the codebase against the PRD, then `group-design` to formulate candidate designs. |
| **ACloud** (architect-cloud) | ACore output + `deep-research` to determine the feature's side effects on cloud deployment. |
| **ASolution** (architect-solution) | ACore output + `deep-research` to place the PRD in enterprise deployments with existing services. |
| **SS** (support-sop) | Builds the SOP from the approved spec: risk mitigation for operating the feature (if X goes wrong, do Y; if you observe Z, do W). |
| **Team** (developer-1..D, test-1..T) | Implement and test the plan. Talk to each other; allocated by the EM. *(TBD)* |

Knowledge repo (artifacts): specs, product-vision*, company-vision*, research, git, market-analysis, github, web, research papers, prds, sops. (*optional)

## Flow

```
PRD ─► EM ─► AExpert ─► ACore: deep-code, then group-design ─► candidate options
                              ├─► ACloud    (ACore output + deep-research)   ┐ parallel
                              └─► ASolution (ACore output + deep-research)   ┘
                        ▼
   AExpert: per-PRD adversarial agents, grounding checks, redo of any of the
   three (cap 2 rounds, then escalate to you)
                        ▼
   GATE 1  you pick an option from the table:
           risk | complexity | future evolution | fit for purpose (succinct, with refs)
                        ▼
   AExpert writes the draft spec to drafts/  (RFC/design-doc + MADR template)
                        ▼
   GATE 2  you review the spec; changes loop back to AExpert
                        ▼
   Approved spec ─► specs/ ─► SS builds the SOP from the spec
                        ▼
   GATE 3  you review the SOP
           └─ changes requested: AExpert re-runs the architecture flow, scoped
              to what you asked for (fresh 2-round cap). If the spec changes,
              it needs re-approval (the delta only).
                        ▼
   Spec approved AND SOP approved ─► SOP written to sops/
                        ▼
   AExpert runs action-plan (parallel by default) ─► EM  (no human review of the plan)
```

## Rules

- **Only AExpert talks to you.**
- **Grounding:** every claim must be grounded in fact (cited). AExpert enforces this.
- **Redo cap:** 2 rounds per request, then AExpert escalates to you.
- **Adversarial angles** are chosen per PRD.
- **Gate to the EM** is approval of the spec AND the SOP.
- **`specs/` holds approved specs only.** Drafts live in `drafts/`.

## Spec template (fixed, always used)

RFC/design-doc style plus a MADR decision record.

- **Metadata:** ID, title, status, author, link to the PRD
- **Sections:**
  - Summary
  - Motivation
  - Goals and non-goals
  - Requirements: IDs (R-1, R-2, ...), RFC 2119 MUST/SHOULD wording
  - Design
  - Alternatives considered (from the option table)
  - Cloud impact
  - Enterprise impact
  - Compatibility and upgrade
  - Risks and mitigations
  - Test strategy and acceptance criteria, traceable to requirement IDs
  - Operational hooks (where the SOP attaches)
  - Open questions
  - References
- **Decision record (MADR):** chosen option, rejected options and why

## Skills

- **Vendored (copied into this repo):** `deep-code`, `group-design`, `action-plan`
- **Referenced, not copied:** `deep-research` from Anthropic's `anthropic-skills`. Installers need that plugin as well.

## Packaging

One distributable skill (skills.sh), one subfolder per role (`architect-chief`, `architect-core`, ...), the vendored skills and the spec template.

## Open

- EM and engineering function (capacity allocation, dev/test collaboration, PRD directory watching)
