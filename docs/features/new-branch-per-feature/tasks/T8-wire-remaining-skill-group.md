---
id: T8
title: "Wire the remaining 11 registered skills to the branch gate"
layer: "wiring"
deps: ["T6"]
blocks: ["T9"]
acs: ["AC-05", "AC-06", "AC-10"]
files_hint: ["skills/plan-tests/SKILL.md", "skills/review/SKILL.md", "skills/roadmap/SKILL.md", "skills/scaffold/SKILL.md", "skills/screens/SKILL.md", "skills/sequences/SKILL.md", "skills/ship/SKILL.md", "skills/specify/SKILL.md", "skills/survey/SKILL.md", "skills/tasks/SKILL.md", "skills/ux-flows/SKILL.md"]
owner: "Tech Lead"
estimate: "8h"
context_budget: "L" # justified: updates 11 separate registered skill entrypoints in one bounded wiring batch.
status: "todo"
step: ""
---

# T8 — Wire the remaining 11 registered skills to the branch gate

## Place in the sequence

- **Blocked by:** T6 — Enforce the shared branch gate at every write boundary · **Blocks:** T9 — Validate branch-gate coverage in CI · **Wave:** 7, parallel with T7 on a disjoint skill-file set.
- **Lane:** own lane across `skills/plan-tests/` through `skills/ux-flows/`; no overlap with T7's skill files.

## Why (user story)

> **As a** Plugin user
> **I want** every SDD skill to check the feature branch across all selected repositories
> **So that** no stage writes or commits feature work on the wrong branch
>
> — `spec.md §4, US-04, verbatim` · full text: [spec.md](../spec.md)

This task adds the shared gate reference to the other eleven registered entrypoints and retains the no-opt-in behavior.

## Inlined context

> Every registered skill invokes the shared gate before any stage write; the gate repeats before feature writes and commits. CI verifies entrypoint coverage.
>
> — `sad.md §5, building block view, abridged` · full text: [sad.md](../sad.md)

> The shared gate is the only required check; host hook capabilities are informational and do not enforce this policy.
>
> — `ADR-0005 §Decision outcome, abridged` · full text: [ADR-0005](../adr/0005-rely-on-the-shared-skill-gate-without-host-hooks.md)

**Fallback:** after T1–T6 establish the canonical `skills/_shared/branch-policy.md`, follow that contract together with [sad.md](../sad.md) §4/§6; do not reorder existing prereq/refusal gates or write boundaries.

## Data delta

No DB changes. This task only wires skill instructions to local policy checks.

— `sad.md §2, technical constraints, abridged` · full text: [sad.md](../sad.md)

## API contract

Internal — no HTTP, CLI, or exported-code API; host-loaded skill workflows are the package surface.

— `ADR-0001 §Decision outcome, verbatim` · full text: [ADR-0001](../adr/0001-treat-the-sdd-plugin-as-a-library-sdk-surface.md)

## Acceptance criteria

### AC-05 — exact branch invariant

> **Given** a feature has an opted-in branch policy with setup marked `active`
> **When** an SDD skill is about to perform a stage write, feature write, or feature commit and a selected repository's active branch does not exactly match the feature slug
> **Then** the skill blocks the affected stage writes and commits and reports the mismatch before the affected write or commit; read-only work and explicit recovery actions remain available
>
> — `spec.md §5, AC-05, verbatim` · full text: [spec.md](../spec.md)

### AC-06 — cross-repository gate

> **Given** a feature spans multiple selected repositories and setup is marked `active`
> **When** any one repository fails a branch check before a stage write, feature write, or feature commit
> **Then** feature writes and commits for the stage are blocked, even if the repository from which it was launched has the correct branch
>
> — `spec.md §5, AC-06, verbatim` · full text: [spec.md](../spec.md)

### AC-10 — no host-hook dependency

> **Given** a feature branch policy has completed setup and the current host does not provide an active blocking hook
> **When** an SDD skill is about to perform a stage write, feature write, or feature commit
> **Then** the shared branch gate verifies the saved policy and blocks writes and commits on mismatches, while read-only work and explicit recovery actions remain available; the policy does not install or rely on host hooks, and any host-specific hook information is informational only
>
> — `spec.md §5, AC-10, verbatim` · full text: [spec.md](../spec.md)

## Checklist

- [ ] Add the shared gate invocation to `skills/plan-tests/SKILL.md`, `skills/review/SKILL.md`, `skills/roadmap/SKILL.md`, `skills/scaffold/SKILL.md`, `skills/screens/SKILL.md`, and `skills/sequences/SKILL.md`.
- [ ] Add it to `skills/ship/SKILL.md`, `skills/specify/SKILL.md`, `skills/survey/SKILL.md`, `skills/tasks/SKILL.md`, and `skills/ux-flows/SKILL.md`.
- [ ] Place it before any stage write and repeat it before feature writes and commits.
- [ ] Preserve every skill's existing behavior when the feature has not opted in.

## Edge cases

| Case | Behaviour |
|---|---|
| Feature policy applies and any selected repository mismatches | Block writes and commits before they occur. |
| Feature has not opted into the policy | Keep the current workflow unchanged. |
| Host lacks a blocking hook | Invoke the shared branch gate anyway. |

## Definition of Done

- [ ] All eleven named entrypoints invoke the shared gate at the required boundaries.
- [ ] No skill-specific duplicate branch-check implementation is introduced.
- [ ] Existing prereq gates, read-only work, and unopted-feature behavior remain intact.
- [ ] Lint + vet clean.
