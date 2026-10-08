# Product guiding principles: <product name>

| | |
|---|---|
| Status | Draft / Approved |
| Owner | <name> |
| Date | <YYYY-MM-DD> |

The words MUST, MUST NOT and SHOULD follow RFC 2119. Architects rule out or flag any option that violates a hard constraint; the Verifier checks them; developers and testers adhere to them.

## 1. Hard constraints
Non-negotiable and verifiable. Repeat the block for each one. IDs are stable once written.

### HC-1: <short name, e.g. Java 21>
- **Constraint:** The code MUST ...
- **Rationale:** why we hold it.
- **Implications:** what it forces and what it forbids.
- **Verification:** the check (lint rule, build setting, benchmark, test) with the exact command or location, or `judgement` if it can only be reviewed.
- **Exceptions:** who may grant one, and how it is recorded.

## 2. Principles
Guide judgement calls. Repeat the block for each one.

### P-1: <short name>
- **Principle:** imperative, testable sentence.
- **Rationale:**
- **Implications:**
- **Verification:** check, or `judgement`.
- **Exceptions:**

## 3. Priority when principles conflict
Ordered list: which wins over which, and why.

## 4. Open questions
