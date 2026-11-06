---
id: T12
title: "Add active-gate and performance evaluation scenarios"
layer: "tests"
deps: ["T6", "T9", "T10", "T11"]
blocks: []
acs: ["AC-05", "AC-06", "AC-07", "AC-10", "AC-11"]
files_hint: ["evals/interactive/branch-policy-gate.md"]
owner: "Tech Lead"
estimate: "8h"
context_budget: "M"
status: "todo"
step: ""
---

# T12 — Add active-gate and performance evaluation scenarios

## Place in the sequence

- **Blocked by:** T6 — Enforce the shared gate; T9 — Validate skill coverage; T10 — Document host-hook information; T11 — Add safe-setup acceptance scenarios · **Blocks:** none · **Wave:** 9, validates the completed workflow, registration, and host guidance.
- **Lane:** own `evals/interactive/branch-policy-gate.md` lane.

## Why (user story)

> **As a** Plugin user
> **I want** every SDD skill to check the feature branch across all selected repositories
> **So that** no stage writes or commits feature work on the wrong branch
>
> — `spec.md §4, US-04, verbatim` · full text: [spec.md](../spec.md)

> **As a** Plugin user
> **I want** project-wide SDD skills to resolve an unambiguous active feature
> **So that** those skills follow the same branch policy as feature-specific stages
>
> — `spec.md §4, US-05, verbatim` · full text: [spec.md](../spec.md)

This task verifies the active gate across repositories and hosts and records the required local preflight benchmark procedure.

## Inlined context

> Any mismatch in any selected repository blocks the stage's feature writes and commits, even when the launch repository is on the correct branch. Read-only inspection and explicit recovery remain available.
>
> — `spec.md §5, AC-05 and AC-06, abridged` · full text: [spec.md](../spec.md)

> Branch preflight latency target: p95 ≤ 2 seconds per selected repository, excluding branch creation and owner interaction. Measure 30 preflight runs against local fixtures containing 1, 3, and 10 repositories.
>
> — `spec.md §6, Branch preflight latency, abridged` · full text: [spec.md](../spec.md)

**Fallback:** use [sad.md](../sad.md) §6 and the host-neutral constraints in [ADR-0005](../adr/0005-rely-on-the-shared-skill-gate-without-host-hooks.md); this matrix verifies skill behavior, not arbitrary direct Git operations.

## Data delta

No DB changes. The test matrix uses local policy JSON and disposable Git repositories.

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

### AC-07 — project-wide feature resolution

> **Given** an SDD skill is invoked without a feature slug while branch policies are in use (a project-wide invocation)
> **When** local project state marks exactly one feature as active, or marks none or multiple features as active
> **Then** the skill uses the one explicitly active feature or requests an explicit feature slug, respectively, and does not proceed with feature writes or commits while the feature remains ambiguous. An active feature is one explicitly selected as active in local project state; it remains active until the user changes that selection
>
> — `spec.md §5, AC-07, verbatim` · full text: [spec.md](../spec.md)

### AC-10 — no host-hook dependency

> **Given** a feature branch policy has completed setup and the current host does not provide an active blocking hook
> **When** an SDD skill is about to perform a stage write, feature write, or feature commit
> **Then** the shared branch gate verifies the saved policy and blocks writes and commits on mismatches, while read-only work and explicit recovery actions remain available; the policy does not install or rely on host hooks, and any host-specific hook information is informational only
>
> — `spec.md §5, AC-10, verbatim` · full text: [spec.md](../spec.md)

### AC-11 — unopted feature compatibility

> **Given** a feature has not opted into `new_branch_per_feature`
> **When** the Plugin user runs an SDD skill
> **Then** the existing workflow, including the legacy `branch_strategy` behavior, remains unchanged
>
> — `spec.md §5, AC-11, verbatim` · full text: [spec.md](../spec.md)

## Checklist

- [ ] Create `evals/interactive/branch-policy-gate.md` with opt-in active-branch, mismatch, multi-repository, ambiguous project-wide feature, and no-opt-in scenarios.
- [ ] For each scenario, assert no feature artifact write or commit occurs before a failed check; separately verify read-only/recovery remains available.
- [ ] Include the complete 23-entrypoint inventory, using the CI validator as the exhaustive check and representative SDD invocations for each supported host.
- [ ] Define a local benchmark procedure for 30 preflight runs with 1, 3, and 10 selected repositories; record per-repository p95 and exclude owner interaction and branch creation.

## Edge cases

| Case | Behaviour |
|---|---|
| Launch checkout matches but another selected checkout does not | Block the feature writes and commits for the stage. |
| No feature slug and zero or multiple active selections | Request an explicit slug and block feature writes and commits. |
| No opt-in exists | Existing `branch_strategy` workflow remains unchanged. |
| No host hook is active | Shared gate still blocks mismatches. |

## Definition of Done

- [ ] Scenarios assert AC-05, AC-06, AC-07, AC-10, and AC-11 outcomes.
- [ ] The evaluation records host, skill entrypoint, selected repository count, branch state, artifact writes, commits, and recovery outcome.
- [ ] Benchmark instructions measure the stated p95 target without including excluded work.
- [ ] Evaluation results stay local and do not introduce telemetry.
