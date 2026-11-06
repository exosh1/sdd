---
id: T11
title: "Add safe-setup acceptance scenarios"
layer: "tests"
deps: ["T5"]
blocks: ["T12"]
acs: ["AC-03", "AC-04", "AC-08", "AC-09", "AC-12"]
files_hint: ["evals/interactive/branch-policy-setup.md"]
owner: "Tech Lead"
estimate: "6h"
context_budget: "M"
status: "todo"
step: ""
---

# T11 — Add safe-setup acceptance scenarios

## Place in the sequence

- **Blocked by:** T5 — Create feature branches and resume pending setup · **Blocks:** T12 — Add active-gate and performance evaluation scenarios · **Wave:** 8, defines runnable manual checks after setup behavior exists.
- **Lane:** own `evals/interactive/branch-policy-setup.md` lane.

## Why (user story)

> **As a** Plugin user
> **I want** branch setup to stop when a repository is not in an approved state
> **So that** existing work and branches are not silently disturbed
>
> — `spec.md §4, US-03, verbatim` · full text: [spec.md](../spec.md)

This task records a host-driven setup matrix so unsafe cases can be verified without assuming an executable runtime checker.

## Inlined context

> Setup safety is verified manually with disposable local Git repositories in each supported host. Failures must occur before feature writes or commits, and preflight latency excludes branch creation and owner interaction.
>
> — `spec.md §5, AC-03; spec.md §6, Unsafe-state enforcement, abridged` · full text: [spec.md](../spec.md)

> The shared procedure is expressed in Markdown; no application runtime or branch-check executable is required in consumer repositories.
>
> — `ADR-0002 §Decision outcome, abridged` · full text: [ADR-0002](../adr/0002-use-shared-instructions-for-branch-checks.md)

**Fallback:** use [evals/README.md](../../../../evals/README.md) for existing evaluation conventions and [sad.md](../sad.md) §6 for setup sequencing.

## Data delta

No DB changes. Acceptance scenarios use disposable local Git repositories.

— `sad.md §2, technical constraints, abridged` · full text: [sad.md](../sad.md)

## API contract

Internal — no HTTP, CLI, or exported-code API; host-loaded skill workflows are the package surface.

— `sad.md §4, target surface, abridged` · full text: [sad.md](../sad.md)

## Acceptance criteria

### AC-03 — unsafe setup state

> **Given** branch setup is needed and a selected repository has any of these unsafe states: tracked changes (staged or unstaged), untracked non-ignored files, a current branch that is neither an allowed base nor the locally recorded default branch, or an existing feature branch that is not active
> **When** the user starts an SDD stage
> **Then** the stage stops before feature work, reports the affected repository and reason, and does not automatically switch to an existing branch, stash, reset, or remove work
>
> — `spec.md §5, AC-03, verbatim` · full text: [spec.md](../spec.md)

### AC-04 — local write authorization

> **Given** the Plugin user lacks local write permission for required policy-state, checkout-identity, or branch setup writes in a selected repository
> **When** the plugin initializes or resumes the feature policy
> **Then** it stops before writing feature artifacts, reports the result for every selected repository, and preserves any branches already created
>
> — `spec.md §5, AC-04, verbatim` · full text: [spec.md](../spec.md)

### AC-08 — invalid saved repository

> **Given** a saved repository path is missing, no longer identifies the same repository, or identifies only an ordinary directory
> **When** a feature stage checks its saved selection
> **Then** the stage stops and asks the Plugin user to choose a valid repository again rather than silently substituting its parent or another repository
>
> — `spec.md §5, AC-08, verbatim` · full text: [spec.md](../spec.md)

### AC-09 — partial branch-creation failure

> **Given** all selected repositories pass setup preflight but branch creation fails partway through
> **When** the plugin reports the failure
> **Then** it lists the state of each selected repository, leaves already-created branches intact, and performs no feature-stage work; a later run resumes setup only after every selected repository passes preflight. If a previously created feature branch is not active, the user must activate it manually before retrying; the plugin never resumes by switching branches
>
> — `spec.md §5, AC-09, verbatim` · full text: [spec.md](../spec.md)

### AC-12 — allowed branch base

> **Given** a selected repository needs a new feature branch
> **When** the plugin checks the current branch as the base
> **Then** it accepts a current branch whose name begins with the case-sensitive literal prefix `main`, `master`, `develop`, or `release`; otherwise it accepts only an exact match for the default branch recorded in that checkout, and stops if neither condition holds
>
> — `spec.md §5, AC-12, verbatim` · full text: [spec.md](../spec.md)

## Checklist

- [ ] Create a manual matrix in `evals/interactive/branch-policy-setup.md` for clean approved bases, disallowed bases, dirty tracked/untracked state, existing inactive target branch, and invalid saved selection.
- [ ] Include a local write-permission failure case and assert per-repository reporting with no feature artifact writes.
- [ ] Include a partial branch-creation failure and retry case; assert prior branches remain and manual activation is required.
- [ ] Name the supported hosts and record observed branch, artifact, and commit state for each run.

## Edge cases

| Case | Behaviour |
|---|---|
| Staged or unstaged tracked changes, or untracked non-ignored files | Setup blocks before mutation. |
| Default branch matches exactly but does not use an allowed prefix | It is accepted only when it exactly matches the local recorded default. |
| Permission failure follows a completed branch creation elsewhere | Report all repositories and preserve the created branch. |
| Saved path is replaced by another checkout | Require explicit reselection; do not identify by name or parent directory. |

## Definition of Done

- [ ] Matrix cases directly exercise AC-03, AC-04, AC-08, AC-09, and AC-12.
- [ ] Each case has a setup state, invocation, expected report, and artifact/branch assertion.
- [ ] Recovery steps do not instruct automatic checkout, stash, reset, or deletion.
- [ ] Markdown links and formatting validate.
