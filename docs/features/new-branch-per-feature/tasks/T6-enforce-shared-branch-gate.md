---
id: T6
title: "Enforce the shared branch gate at every write boundary"
layer: "app"
deps: ["T1", "T5"]
blocks: ["T7", "T8", "T10", "T12"]
acs: ["AC-05", "AC-06", "AC-10"]
files_hint: ["skills/_shared/branch-policy.md"]
owner: "Tech Lead"
estimate: "6h"
context_budget: "L" # justified: the gate's inlined contract is constrained by five upstream artifacts.
status: "todo"
step: ""
---

# T6 — Enforce the shared branch gate at every write boundary

## Place in the sequence

- **Blocked by:** T1 — Define local policy state and active-feature resolution; T5 — Create feature branches and resume pending setup · **Blocks:** T7 — Wire first 12 skills; T8 — Wire remaining 11 skills; T10 — Document host-hook information; T12 — Evaluate gate and performance · **Wave:** 6, defines the common gate consumed by entrypoints.
- **Lane:** shared `skills/_shared/branch-policy.md` lane with T1–T5; serialized.

## Why (user story)

> **As a** Plugin user
> **I want** every SDD skill to check the feature branch across all selected repositories
> **So that** no stage writes or commits feature work on the wrong branch
>
> — `spec.md §4, US-04, verbatim` · full text: [spec.md](../spec.md)

This task specifies the shared preflight and repeat-check contract used by all 23 skill entrypoints.

## Inlined context

> Require one shared branch gate before any stage write, including settings/bootstrap/status changes, and repeat it before feature writes and commits. CI verifies entrypoint coverage. Do not require a consumer runtime or executable helper.
>
> — `ADR-0002 §Decision outcome, abridged` · full text: [ADR-0002](../adr/0002-use-shared-instructions-for-branch-checks.md)

> Every selected repository must be on the exact feature-slug branch before feature work. A failure in any repository blocks all stage writes and commits; read-only inspection and explicit recovery remain available.
>
> — `spec.md §5, AC-05 and AC-06, abridged` · full text: [spec.md](../spec.md)

**Fallback:** read [ADR-0002](../adr/0002-use-shared-instructions-for-branch-checks.md), [ADR-0005](../adr/0005-rely-on-the-shared-skill-gate-without-host-hooks.md), and [sad.md](../sad.md) §6 before changing the gate contract.

## Data delta

No DB changes. The gate reads local policy JSON and local Git state.

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

- [ ] Specify gate invocation before every stage write and repeat-check before each feature write and commit.
- [ ] Check all selected repositories as one atomic authorization set; report each mismatch and block the affected operation.
- [ ] Preserve read-only inspection and explicit recovery after a gate failure.
- [ ] State that host hooks are not installed or relied on in `skills/_shared/branch-policy.md`.

## Edge cases

| Case | Behaviour |
|---|---|
| Launch checkout matches but another selected checkout does not | Block the whole stage's feature writes and commits. |
| A branch changes after initial stage preflight | Recheck and block the imminent write or commit. |
| Host has no active blocking hook | Shared skill gate still checks and enforces the policy. |
| Policy is not opted in | Preserve the legacy workflow defined by T1. |

## Definition of Done

- [ ] Before-write and before-commit checks satisfy AC-05.
- [ ] Any selected-repository mismatch blocks the stage as required by AC-06.
- [ ] No host hook is installed, required, or treated as enforcement under AC-10.
- [ ] Lint + vet clean.
