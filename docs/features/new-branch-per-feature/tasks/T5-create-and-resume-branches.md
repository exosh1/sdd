---
id: T5
title: "Create feature branches and resume pending setup"
layer: "app"
deps: ["T4"]
blocks: ["T6", "T11"]
acs: ["AC-01", "AC-09"]
files_hint: ["skills/_shared/branch-policy.md"]
owner: "Tech Lead"
estimate: "6h"
context_budget: "M"
status: "todo"
step: ""
---

# T5 — Create feature branches and resume pending setup

## Place in the sequence

- **Blocked by:** T4 — Record checkout identity and verify local write access · **Blocks:** T6 — Enforce the shared branch gate at every write boundary; T11 — Add safe-setup acceptance evaluation scenarios · **Wave:** 5, applies mutations only after all selected repositories pass preflight.
- **Lane:** shared `skills/_shared/branch-policy.md` lane with T1–T6; serialized.

## Why (user story)

> **As a** Plugin user
> **I want** to opt a feature into its own branch policy
> **So that** its planning and implementation work stays separate from other work
>
> — `spec.md §4, US-01, verbatim` · full text: [spec.md](../spec.md)

> **As a** Plugin user
> **I want** branch setup to stop when a repository is not in an approved state
> **So that** existing work and branches are not silently disturbed
>
> — `spec.md §4, US-03, verbatim` · full text: [spec.md](../spec.md)

This task creates missing exact-slug branches without checking them out and preserves resumable pending state after partial setup.

## Inlined context

> Save the policy as `pending` before creating missing branches. Branch creation never checks out a branch. The Plugin user activates target branches manually; only a complete all-repository branch check changes setup to `active`. Preserve already-created branches on failure and require manual activation before retry.
>
> — `sad.md §6, Critical flow 1, abridged` · full text: [sad.md](../sad.md)

> **Given** all selected repositories pass setup preflight but branch creation fails partway through
> **When** the plugin reports the failure
> **Then** it lists the state of each selected repository, leaves already-created branches intact, and performs no feature-stage work; a later run resumes setup only after every selected repository passes preflight. If a previously created feature branch is not active, the user must activate it manually before retrying; the plugin never resumes by switching branches
>
> — `spec.md §5, AC-09, verbatim` · full text: [spec.md](../spec.md)

**Fallback:** use [spec.md](../spec.md) §1 and [sad.md](../sad.md) §6 for full setup order; never add automatic checkout or rollback.

## Data delta

No DB changes. Setup persists local branch policy state and local Git branches.

— `ADR-0003 §Decision outcome, abridged` · full text: [ADR-0003](../adr/0003-store-policy-in-an-ignored-project-json-file.md)

## API contract

Internal — no HTTP, CLI, or exported-code API; host-loaded skill workflows are the package surface.

— `ADR-0001 §Decision outcome, verbatim` · full text: [ADR-0001](../adr/0001-treat-the-sdd-plugin-as-a-library-sdk-surface.md)

## Acceptance criteria

### AC-01 — initialize feature policy

> **Given** a Plugin user starts a feature with `new_branch_per_feature` and completes repository selection
> **When** the first feature stage initializes the policy
> **Then** the plugin creates any missing local branch named exactly for the feature slug without checking it out, saves the policy and selection in local project state that remains readable from any branch with setup marked `pending`, and leaves unselected repositories unchanged; the Plugin user must activate the target branch manually in every selected repository, and no feature-stage work starts until all selected repositories are on that branch and setup is marked `active`
>
> — `spec.md §5, AC-01, verbatim` · full text: [spec.md](../spec.md)

### AC-09 — partial branch-creation failure

> **Given** all selected repositories pass setup preflight but branch creation fails partway through
> **When** the plugin reports the failure
> **Then** it lists the state of each selected repository, leaves already-created branches intact, and performs no feature-stage work; a later run resumes setup only after every selected repository passes preflight. If a previously created feature branch is not active, the user must activate it manually before retrying; the plugin never resumes by switching branches
>
> — `spec.md §5, AC-09, verbatim` · full text: [spec.md](../spec.md)

## Checklist

- [ ] Save pending policy state with complete repository selection and checkout UUID map before branch creation.
- [ ] Create only missing exact-slug local branches, from the approved current base, without checkout.
- [ ] Preserve already-created branches and report each selected repository when setup fails partway through.
- [ ] Keep setup pending until all selected repositories are manually on the target branch and a full check succeeds.

## Edge cases

| Case | Behaviour |
|---|---|
| Branch creation fails after earlier repositories succeed | Preserve completed branches, report every repository, and perform no feature-stage work. |
| A target branch exists but is not active during retry | Stop; require manual activation before retrying. |
| All selected repositories are already on the target branch | Verify them and mark setup active only after the complete check passes. |
| An unselected repository exists in the workspace | Leave it unchanged. |

## Definition of Done

- [ ] Setup ordering and successful activation satisfy AC-01.
- [ ] Partial failure and retry behavior satisfy AC-09.
- [ ] No automatic checkout, switch, rollback, stash, reset, or branch deletion is performed.
- [ ] Lint + vet clean.
