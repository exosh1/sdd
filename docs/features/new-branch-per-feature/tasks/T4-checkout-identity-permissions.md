---
id: T4
title: "Record checkout identity and verify local write access"
layer: "app"
deps: ["T3"]
blocks: ["T5"]
acs: ["AC-04"]
files_hint: ["skills/_shared/branch-policy.md"]
owner: "Tech Lead"
estimate: "4h"
context_budget: "M"
status: "todo"
step: ""
---

# T4 — Record checkout identity and verify local write access

## Place in the sequence

- **Blocked by:** T3 — Enforce safe branch-setup preflight · **Blocks:** T5 — Create feature branches and resume pending setup · **Wave:** 4, runs after the complete repository preflight.
- **Lane:** shared `skills/_shared/branch-policy.md` lane with T1–T6; serialized.

## Why (user story)

> **As a** Plugin user
> **I want** branch setup to stop when a repository is not in an approved state
> **So that** existing work and branches are not silently disturbed
>
> — `spec.md §4, US-03, verbatim` · full text: [spec.md](../spec.md)

This task makes setup report permission failures across the selected set before writing feature artifacts.

## Inlined context

> Assign each selected checkout a random local UUID stored in its Git configuration, and store the UUID with its canonical path in `.sdd/branch-policy.json`. If the saved path is missing or the UUID does not match, stop and require explicit reselection; never locate or substitute a repository by name.
>
> — `ADR-0004 §Decision outcome, verbatim` · full text: [ADR-0004](../adr/0004-identify-checkouts-with-a-local-git-uuid.md)

> Setup checks local write access for policy-state, checkout-identity, and branch setup writes; failures are visible and stop before feature artifacts.
>
> — `spec.md §6.1, AuthZ/AuthN impact, abridged` · full text: [spec.md](../spec.md)

**Fallback:** use [ADR-0004](../adr/0004-identify-checkouts-with-a-local-git-uuid.md) for identity and [sad.md](../sad.md) §6 for setup ordering; do not inspect remotes.

## Data delta

No DB changes. Checkout identity is stored in each selected checkout's local Git configuration and policy JSON.

— `ADR-0004 §Decision outcome, abridged` · full text: [ADR-0004](../adr/0004-identify-checkouts-with-a-local-git-uuid.md)

## API contract

Internal — no HTTP, CLI, or exported-code API; host-loaded skill workflows are the package surface.

— `ADR-0001 §Decision outcome, verbatim` · full text: [ADR-0001](../adr/0001-treat-the-sdd-plugin-as-a-library-sdk-surface.md)

## Acceptance criteria

### AC-04 — local write authorization

> **Given** the Plugin user lacks local write permission for required policy-state, checkout-identity, or branch setup writes in a selected repository
> **When** the plugin initializes or resumes the feature policy
> **Then** it stops before writing feature artifacts, reports the result for every selected repository, and preserves any branches already created
>
> — `spec.md §5, AC-04, verbatim` · full text: [spec.md](../spec.md)

## Checklist

- [ ] Check the ability to write local exclude metadata, checkout UUIDs, policy state, and required branch metadata in `skills/_shared/branch-policy.md`.
- [ ] Record/reuse UUIDs only after checkout identity is verified.
- [ ] Report every selected repository's result and stop feature work on any required write-permission failure.
- [ ] Preserve branches already created by an earlier partial setup.

## Edge cases

| Case | Behaviour |
|---|---|
| Git configuration is read-only | Report the affected checkout and stop before feature artifacts. |
| Checkout UUID does not match saved state | Stop and require explicit reselection; never substitute by name. |
| Another repository's metadata write fails | Report all selected repositories and preserve safe prior writes. |

## Definition of Done

- [ ] Permission preflight and visible failure results satisfy AC-04.
- [ ] Identity behavior matches ADR-0004 and does not depend on remotes.
- [ ] Required local metadata writes occur only after the setup preflight passes.
- [ ] Lint + vet clean.
