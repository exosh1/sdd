---
id: T2
title: "Discover and explicitly select eligible repositories"
layer: "app"
deps: ["T1"]
blocks: ["T3"]
acs: ["AC-02", "AC-08"]
files_hint: ["skills/_shared/branch-policy.md"]
owner: "Tech Lead"
estimate: "6h"
context_budget: "M"
status: "todo"
step: ""
---

# T2 — Discover and explicitly select eligible repositories

## Place in the sequence

- **Blocked by:** T1 — Define local policy state and active-feature resolution · **Blocks:** T3 — Enforce safe branch-setup preflight · **Wave:** 2, builds selection on the policy-state contract.
- **Lane:** shared `skills/_shared/branch-policy.md` lane with T1 and T3–T6; serialized.

## Why (user story)

> **As a** Plugin user
> **I want** to choose which independent repositories participate in a feature
> **So that** unrelated repositories remain untouched
>
> — `spec.md §4, US-02, verbatim` · full text: [spec.md](../spec.md)

This task defines safe discovery and explicit selection, including reselection instead of silently substituting an invalid saved path.

## Inlined context

> Repository discovery stays within the project workspace unless the owner explicitly selects another canonical Git root. The documents repository is mandatory; no other repository is chosen implicitly. Exclude submodules and linked worktrees.
>
> — `spec.md §1, owner-confirmed constraints; spec.md §5, AC-02, abridged` · full text: [spec.md](../spec.md)

> **Given** a saved repository path is missing, no longer identifies the same repository, or identifies only an ordinary directory
> **When** a feature stage checks its saved selection
> **Then** the stage stops and asks the Plugin user to choose a valid repository again rather than silently substituting its parent or another repository
>
> — `spec.md §5, AC-08, verbatim` · full text: [spec.md](../spec.md)

**Fallback:** use [spec.md](../spec.md) §6.1 and [ADR-0003](../adr/0003-store-policy-in-an-ignored-project-json-file.md) for the full path and state constraints; never infer a replacement repository.

## Data delta

No DB changes. Repository selections are stored in local policy JSON.

— `sad.md §4, solution strategy decision 2, abridged` · full text: [sad.md](../sad.md)

## API contract

Internal — no HTTP, CLI, or exported-code API; host-loaded skill workflows are the package surface.

— `ADR-0001 §Decision outcome, verbatim` · full text: [ADR-0001](../adr/0001-treat-the-sdd-plugin-as-a-library-sdk-surface.md)

## Acceptance criteria

### AC-02 — explicit repository selection

> **Given** a Plugin user enables the policy in a project workspace
> **When** the plugin recursively discovers independent Git checkouts within that workspace or validates paths explicitly provided by the user
> **Then** it excludes submodules and linked worktrees from eligible repositories, and the user can explicitly choose repositories using checkboxes or a numbered text fallback; the repository containing the feature's SDD documents is mandatory, and no other repository is chosen implicitly
>
> — `spec.md §5, AC-02, verbatim` · full text: [spec.md](../spec.md)

### AC-08 — invalid saved repository

> **Given** a saved repository path is missing, no longer identifies the same repository, or identifies only an ordinary directory
> **When** a feature stage checks its saved selection
> **Then** the stage stops and asks the Plugin user to choose a valid repository again rather than silently substituting its parent or another repository
>
> — `spec.md §5, AC-08, verbatim` · full text: [spec.md](../spec.md)

## Checklist

- [ ] Specify recursive discovery boundaries and eligibility checks in `skills/_shared/branch-policy.md`.
- [ ] Require explicit selection and the documents checkout; describe checkbox and numbered-text fallback.
- [ ] Validate explicit and saved paths as data and require reselection when a saved checkout is missing or changed.

## Edge cases

| Case | Behaviour |
|---|---|
| A discovered checkout is a submodule or linked worktree | Exclude it from eligible choices. |
| A path points outside the workspace without explicit selection | Reject it before Git operations. |
| A saved path is missing, replaced, or an ordinary directory | Stop and ask for an explicit valid repository selection. |

## Definition of Done

- [ ] Discovery and explicit selection rules satisfy AC-02.
- [ ] Invalid saved selections satisfy AC-08 without parent or name-based fallback.
- [ ] The feature documents repository-path validation as data, not command input.
- [ ] Lint + vet clean.
