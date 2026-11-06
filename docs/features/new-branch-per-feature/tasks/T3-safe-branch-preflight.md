---
id: T3
title: "Enforce safe branch-setup preflight"
layer: "app"
deps: ["T2"]
blocks: ["T4"]
acs: ["AC-03", "AC-12"]
files_hint: ["skills/_shared/branch-policy.md"]
owner: "Tech Lead"
estimate: "6h"
context_budget: "M"
status: "todo"
step: ""
---

# T3 — Enforce safe branch-setup preflight

## Place in the sequence

- **Blocked by:** T2 — Discover and explicitly select eligible repositories · **Blocks:** T4 — Record checkout identity and verify local write access · **Wave:** 3, preflights the selected set before setup mutations.
- **Lane:** shared `skills/_shared/branch-policy.md` lane with T1–T6; serialized.

## Why (user story)

> **As a** Plugin user
> **I want** branch setup to stop when a repository is not in an approved state
> **So that** existing work and branches are not silently disturbed
>
> — `spec.md §4, US-03, verbatim` · full text: [spec.md](../spec.md)

This task makes setup fail safely before any mutation when the working tree or branch base is unsafe.

## Inlined context

> Create a missing exact feature-slug branch only from a clean current branch whose name begins with the case-sensitive literal prefix `main`, `master`, `develop`, or `release`, or exactly matches that checkout's locally recorded default branch. An existing target branch that is not active blocks setup and requires manual activation.
>
> — `sad.md §4, solution strategy decision 3, abridged` · full text: [sad.md](../sad.md)

> **Given** branch setup is needed and a selected repository has any of these unsafe states: tracked changes (staged or unstaged), untracked non-ignored files, a current branch that is neither an allowed base nor the locally recorded default branch, or an existing feature branch that is not active
> **When** the user starts an SDD stage
> **Then** the stage stops before feature work, reports the affected repository and reason, and does not automatically switch to an existing branch, stash, reset, or remove work
>
> — `spec.md §5, AC-03, verbatim` · full text: [spec.md](../spec.md)

**Fallback:** consult [spec.md](../spec.md) §1 and [sad.md](../sad.md) §6 for complete setup semantics; do not broaden the allowed base prefixes.

## Data delta

No DB changes. Preflight reads local Git state and does not add schema.

— `sad.md §2, technical constraints, abridged` · full text: [sad.md](../sad.md)

## API contract

Internal — no HTTP, CLI, or exported-code API; host-loaded skill workflows are the package surface.

— `ADR-0001 §Decision outcome, verbatim` · full text: [ADR-0001](../adr/0001-treat-the-sdd-plugin-as-a-library-sdk-surface.md)

## Acceptance criteria

### AC-03 — unsafe setup state

> **Given** branch setup is needed and a selected repository has any of these unsafe states: tracked changes (staged or unstaged), untracked non-ignored files, a current branch that is neither an allowed base nor the locally recorded default branch, or an existing feature branch that is not active
> **When** the user starts an SDD stage
> **Then** the stage stops before feature work, reports the affected repository and reason, and does not automatically switch to an existing branch, stash, reset, or remove work
>
> — `spec.md §5, AC-03, verbatim` · full text: [spec.md](../spec.md)

### AC-12 — allowed branch base

> **Given** a selected repository needs a new feature branch
> **When** the plugin checks the current branch as the base
> **Then** it accepts a current branch whose name begins with the case-sensitive literal prefix `main`, `master`, `develop`, or `release`; otherwise it accepts only an exact match for the default branch recorded in that checkout, and stops if neither condition holds
>
> — `spec.md §5, AC-12, verbatim` · full text: [spec.md](../spec.md)

## Checklist

- [ ] Define one read-only preflight pass across every selected checkout in `skills/_shared/branch-policy.md`.
- [ ] Reject staged/unstaged tracked changes and untracked non-ignored files when a new branch is needed.
- [ ] Accept only the specified case-sensitive base prefixes or the exact local default branch.
- [ ] Reject an existing inactive target branch and report the repository plus manual recovery action.

## Edge cases

| Case | Behaviour |
|---|---|
| A repository is already on the exact feature branch | Verify identity and branch; a dirty worktree is allowed. |
| A repository needs a new branch but has non-ignored work | Stop before setup writes. |
| An existing target branch is not active | Require manual activation; never switch automatically. |
| Current branch is not an allowed base or exact local default | Stop without creating a branch. |

## Definition of Done

- [ ] All preflight outcomes satisfy AC-03 and AC-12.
- [ ] The preflight is read-only and reports each failing repository.
- [ ] No automatic switch, stash, reset, or cleanup path is specified.
- [ ] Lint + vet clean.
