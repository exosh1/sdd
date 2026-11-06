---
id: T1
title: "Define local policy state and active-feature resolution"
layer: "app"
deps: []
blocks: ["T2", "T6"]
acs: ["AC-07", "AC-11"]
files_hint: ["skills/_shared/branch-policy.md"]
owner: "Tech Lead"
estimate: "6h"
context_budget: "M"
status: "todo"
step: ""
---

# T1 — Define local policy state and active-feature resolution

## Place in the sequence

- **Blocked by:** none · **Blocks:** T2 — Discover and explicitly select eligible repositories; T6 — Enforce the shared branch gate at every write boundary · **Wave:** 1, establishes the state contract.
- **Lane:** shared `skills/_shared/branch-policy.md` lane with T2–T6; serialized with those tasks.

## Why (user story)

> **As a** Plugin user
> **I want** project-wide SDD skills to resolve an unambiguous active feature
> **So that** those skills follow the same branch policy as feature-specific stages
>
> — `spec.md §4, US-05, verbatim` · full text: [spec.md](../spec.md)

> **As a** Plugin user
> **I want** to opt a feature into its own branch policy
> **So that** its planning and implementation work stays separate from other work
>
> — `spec.md §4, US-01, verbatim` · full text: [spec.md](../spec.md)

This task defines how the gate reads opt-in state and resolves the explicitly active feature without changing non-opted-in workflows.

## Inlined context

> Store per-feature opt-in, selected repositories, active-feature selection, and setup status in branch-independent local state. Missing policy means no opt-in; expected but missing, malformed, or unreadable opted-in state fails closed.
>
> — `sad.md §4, solution strategy decision 2, abridged` · full text: [sad.md](../sad.md)

> **Given** an SDD skill is invoked without a feature slug while branch policies are in use (a project-wide invocation)
> **When** local project state marks exactly one feature as active, or marks none or multiple features as active
> **Then** the skill uses the one explicitly active feature or requests an explicit feature slug, respectively, and does not proceed with feature writes or commits while the feature remains ambiguous. An active feature is one explicitly selected as active in local project state; it remains active until the user changes that selection
>
> — `spec.md §5, AC-07, verbatim` · full text: [spec.md](../spec.md)

**Fallback:** if the implementing behavior conflicts with the feature artifacts, read the full [spec.md](../spec.md), [sad.md](../sad.md), and [ADR-0003](../adr/0003-store-policy-in-an-ignored-project-json-file.md).

## Data delta

No DB changes. Policy state is local JSON and Git metadata, not a database schema.

— `sad.md §2, technical constraints, abridged` · full text: [sad.md](../sad.md)

## API contract

Internal — no HTTP, CLI, or exported-code API; host-loaded skill workflows are the package surface.

— `ADR-0001 §Decision outcome, verbatim` · full text: [ADR-0001](../adr/0001-treat-the-sdd-plugin-as-a-library-sdk-surface.md)

## Acceptance criteria

### AC-07 — project-wide feature resolution

> **Given** an SDD skill is invoked without a feature slug while branch policies are in use (a project-wide invocation)
> **When** local project state marks exactly one feature as active, or marks none or multiple features as active
> **Then** the skill uses the one explicitly active feature or requests an explicit feature slug, respectively, and does not proceed with feature writes or commits while the feature remains ambiguous. An active feature is one explicitly selected as active in local project state; it remains active until the user changes that selection
>
> — `spec.md §5, AC-07, verbatim` · full text: [spec.md](../spec.md)

### AC-11 — unopted feature compatibility

> **Given** a feature has not opted into `new_branch_per_feature`
> **When** the Plugin user runs an SDD skill
> **Then** the existing workflow, including the legacy `branch_strategy` behavior, remains unchanged
>
> — `spec.md §5, AC-11, verbatim` · full text: [spec.md](../spec.md)

## Checklist

- [ ] Define local policy fields, setup states, and explicit active-feature selection in `skills/_shared/branch-policy.md`.
- [ ] Specify the no-opt-in legacy no-op and the fail-closed behavior for expected invalid state in `skills/_shared/branch-policy.md`.
- [ ] Specify explicit-slug recovery when project-wide feature resolution finds zero or multiple active features.

## Edge cases

| Case | Behaviour |
|---|---|
| No policy applies and no opt-in is requested | Keep the legacy workflow unchanged. |
| Expected opted-in state is missing, malformed, or unreadable | Fail closed before feature writes or commits. |
| Project-wide invocation has zero or multiple explicitly active features | Request an explicit slug and block feature writes and commits. |

## Definition of Done

- [ ] State fields and resolution rules are defined in the shared policy contract.
- [ ] AC-07 and AC-11 outcomes are explicit and testable.
- [ ] No database or host-specific policy state is introduced.
- [ ] Lint + vet clean.
