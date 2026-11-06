---
status: Accepted
owner: "Tech Lead"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-06"
feature_size: "M"
ticket: "Not provided"
---

# 0001 — Treat the SDD plugin as a library-sdk surface

- **Status:** Accepted
- **Date:** 2026-11-06
- **Deciders:** Tech Lead and Plugin user

## Context

The feature adds branch isolation to the SDD plugin package, which is loaded by multiple AI coding hosts. The surface taxonomy has no explicit plugin category, and the package does not introduce a standalone terminal application or user-facing interface. A single target surface is required so downstream stages choose the right contract and task artifacts.

## Decision drivers

- The spec requires the policy to apply across all 23 registered SDD skills.
- The existing repository is a cross-host plugin package, not an application service.
- The target surface must describe the package interface without inventing a UI.

## Considered options

1. **`library-sdk`** — model the reusable host-loaded plugin package as its exposed skill interface.
2. **`cli`** — model the feature as terminal commands with command-line arguments and exit codes.
3. **`library-sdk` and `cli`** — declare both package and terminal surfaces.

## Decision outcome

**Chosen:** `library-sdk`. The plugin is consumed through host-loaded SDD skill workflows, not a standalone CLI; one surface avoids creating a contract and task layer for a nonexistent terminal application.

## Consequences

**Positive**
- Downstream stages have one explicit, machine-readable surface.
- No UI-architecture decision or screen artifact is implied.

**Negative**
- `library-sdk` is the closest available taxonomy value rather than a purpose-built plugin surface.
- Future plugin-specific surface types may require extending the shared taxonomy.

**Neutral**
- The surface declaration can be revised if the plugin later adds a true standalone CLI or another independently owned container.

## Links

- Spec: [[../spec.md]]
- SAD: [[../sad.md]] §4
- Related ADR: —
