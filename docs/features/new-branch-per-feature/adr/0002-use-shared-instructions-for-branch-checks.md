---
status: Accepted
owner: "Tech Lead"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-06"
feature_size: "M"
ticket: "Not provided"
---

# 0002 — Use shared instructions for branch checks

- **Status:** Accepted
- **Date:** 2026-11-06
- **Deciders:** Tech Lead and Plugin user

## Context

The package has no runtime middleware; cross-skill behavior is expressed through shared Markdown contracts that each skill references. Branch checks must work across all registered skills and hosts, including when a host hook is unavailable. The spec requires the branch-state procedure to be deterministic and to fail before feature writes or commits.

## Decision drivers

- The spec targets 100% unsafe-state blocking before feature writes or commits.
- CI can verify that every registered skill invokes the shared gate.
- The current package uses shared instruction files for cross-skill contracts and avoids imposing a runtime on consumer projects.

## Considered options

1. **Shared instructions** — define Git preflight steps in one shared contract and require each skill to invoke it.
2. **Python 3 checker** — add a packaged executable that parses policy state and runs Git checks, failing closed when unavailable.

## Decision outcome

**Chosen:** Shared instructions. Add one shared branch-policy contract and require all skill entrypoints to call it before any stage write and again before feature writes and commits; extend CI validation to catch missing references. Do not require Python 3 or a helper executable in consumer environments.

## Consequences

**Positive**
- Preserves the plugin's host-neutral, documentation-first architecture.
- Avoids requiring a new runtime or locating an installed script across different host layouts.
- Keeps the policy rules in one place instead of distributing distinct implementations.

**Negative**
- CI can prove entrypoint coverage but cannot guarantee that an AI host executes every instruction correctly.
- The shared gate cannot intercept direct file edits or commands outside SDD skill workflows.

**Neutral**
- Host hooks are not part of this decision; their absence does not remove the required skill-level check.

## Links

- Spec: [[../spec.md]]
- SAD: [[../sad.md]] §4
- Related ADR: [[0005-rely-on-the-shared-skill-gate-without-host-hooks]]
