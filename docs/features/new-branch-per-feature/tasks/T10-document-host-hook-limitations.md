---
id: T10
title: "Document host-hook information as non-enforcing"
layer: "docs"
deps: ["T6"]
blocks: ["T12"]
acs: ["AC-10"]
files_hint: ["README.md", "skills/_shared/tool-adapters.md"]
owner: "Tech Lead"
estimate: "3h"
context_budget: "M"
status: "todo"
step: ""
---

# T10 — Document host-hook information as non-enforcing

## Place in the sequence

- **Blocked by:** T6 — Enforce the shared branch gate at every write boundary · **Blocks:** T12 — Add active-gate and performance evaluation scenarios · **Wave:** 7, documentation can proceed in parallel with entrypoint wiring.
- **Lane:** own `README.md` and `skills/_shared/tool-adapters.md` lane.

## Why (user story)

> **As a** Plugin user
> **I want** every SDD skill to check the feature branch across all selected repositories
> **So that** no stage writes or commits feature work on the wrong branch
>
> — `spec.md §4, US-04, verbatim` · full text: [spec.md](../spec.md)

This task prevents users from mistaking host hook documentation for required or active branch-policy enforcement.

## Inlined context

> Do not ship or rely on host-level branch-check hooks. The shared skill gate is the only required check; host hook capabilities may be described as informational context without implying they enforce this policy.
>
> — `ADR-0005 §Decision outcome, verbatim` · full text: [ADR-0005](../adr/0005-rely-on-the-shared-skill-gate-without-host-hooks.md)

> Make clear that the shared skill gate is the only required branch-policy check and that host hook information is informational only.
>
> — `spec.md §6.1, abuse cases, abridged` · full text: [spec.md](../spec.md)

**Fallback:** follow [ADR-0005](../adr/0005-rely-on-the-shared-skill-gate-without-host-hooks.md); do not add installation, configuration, or setup instructions for enforcement hooks.

## Data delta

No DB changes.

— `sad.md §2, technical constraints, abridged` · full text: [sad.md](../sad.md)

## API contract

Internal — no HTTP, CLI, or exported-code API; host-loaded skill workflows are the package surface.

— `ADR-0001 §Decision outcome, verbatim` · full text: [ADR-0001](../adr/0001-treat-the-sdd-plugin-as-a-library-sdk-surface.md)

## Acceptance criteria

### AC-10 — host hook information is informational

> **Given** a feature branch policy has completed setup and the current host does not provide an active blocking hook
> **When** an SDD skill is about to perform a stage write, feature write, or feature commit
> **Then** the shared branch gate verifies the saved policy and blocks writes and commits on mismatches, while read-only work and explicit recovery actions remain available; the policy does not install or rely on host hooks, and any host-specific hook information is informational only
>
> — `spec.md §5, AC-10, verbatim` · full text: [spec.md](../spec.md)

## Checklist

- [ ] Update `README.md` and `skills/_shared/tool-adapters.md` only where host-hook information is relevant.
- [ ] State that host hook capability descriptions are informational, not policy enforcement.
- [ ] Point users to the shared branch gate as the only required enforcement mechanism.
- [ ] Avoid adding hook installation or host-specific blocking scripts.

## Edge cases

| Case | Behaviour |
|---|---|
| A host offers hooks but they are disabled or unavailable | Shared gate remains required and authoritative. |
| A reader interprets host documentation as enforcement | Wording explicitly says hooks are informational only. |
| A proposed documentation change implies hook installation | Exclude it from this feature. |

## Definition of Done

- [ ] User-facing host descriptions preserve the ADR-0005 decision.
- [ ] No host-level branch hook is installed, configured, or required.
- [ ] The shared gate's required status is stated plainly.
- [ ] Documentation links and formatting validate.
