---
id: T9
title: "Validate branch-gate coverage in CI"
layer: "tests"
deps: ["T7", "T8"]
blocks: ["T12"]
acs: ["AC-10"]
files_hint: ["scripts/validate_plugin.py"]
owner: "Tech Lead"
estimate: "4h"
context_budget: "M"
status: "todo"
step: ""
---

# T9 — Validate branch-gate coverage in CI

## Place in the sequence

- **Blocked by:** T7 — Wire first 12 registered skills; T8 — Wire remaining 11 registered skills · **Blocks:** T12 — Add active-gate and performance evaluation scenarios · **Wave:** 8, validates the completed entrypoint wiring.
- **Lane:** own `scripts/validate_plugin.py` lane.

## Why (user story)

> **As a** Plugin user
> **I want** every SDD skill to check the feature branch across all selected repositories
> **So that** no stage writes or commits feature work on the wrong branch
>
> — `spec.md §4, US-04, verbatim` · full text: [spec.md](../spec.md)

This task makes a missing gate reference on any newly registered skill a deterministic CI failure.

## Inlined context

> 100% of registered SDD skills resolve and invoke the shared gate when a feature policy applies. CI validator checks every registered skill entrypoint.
>
> — `spec.md §6, Skill coverage, verbatim` · full text: [spec.md](../spec.md)

> The validator discovers skill entrypoints from `skills/*/SKILL.md` and derives the current registered count from that inventory.
>
> — `scripts/validate_plugin.py, skill registration and count checks, abridged` · full text: [scripts/validate_plugin.py](../../../../scripts/validate_plugin.py)

**Fallback:** extend the existing dynamic discovery in [scripts/validate_plugin.py](../../../../scripts/validate_plugin.py); do not hard-code the current count as the future source of truth.

## Data delta

No DB changes. This is a package-level static validation rule.

— `sad.md §2, technical constraints, abridged` · full text: [sad.md](../sad.md)

## API contract

Internal — no HTTP, CLI, or exported-code API; host-loaded skill workflows are the package surface.

— `ADR-0001 §Decision outcome, verbatim` · full text: [ADR-0001](../adr/0001-treat-the-sdd-plugin-as-a-library-sdk-surface.md)

## Acceptance criteria

### AC-10 — no host-hook dependency

> **Given** a feature branch policy has completed setup and the current host does not provide an active blocking hook
> **When** an SDD skill is about to perform a stage write, feature write, or feature commit
> **Then** the shared branch gate verifies the saved policy and blocks writes and commits on mismatches, while read-only work and explicit recovery actions remain available; the policy does not install or rely on host hooks, and any host-specific hook information is informational only
>
> — `spec.md §5, AC-10, verbatim` · full text: [spec.md](../spec.md)

## Checklist

- [ ] Extend `scripts/validate_plugin.py` to require the canonical branch-policy reference on every discovered registered skill entrypoint.
- [ ] Keep skill discovery dynamic so additions are checked automatically.
- [ ] Report the missing skill path clearly when a gate reference is absent.
- [ ] Keep the existing CI workflow using the validator as its deterministic gate.

## Edge cases

| Case | Behaviour |
|---|---|
| A new skill is registered without the gate reference | Validation fails and identifies its `SKILL.md`. |
| The repository has zero or unexpected skill count | Existing count validation remains dynamic and fails as appropriate. |
| A host has no active blocking hook | Static coverage validation still requires the skill-level gate. |

## Definition of Done

- [ ] Every registered `skills/*/SKILL.md` is checked for the canonical gate invocation.
- [ ] A missing invocation produces a failing validator result naming the entrypoint.
- [ ] Existing skill-count and validator checks continue to pass.
- [ ] Lint + vet clean.
