---
status: Accepted
owner: "Tech Lead"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-06"
feature_size: "M"
ticket: "Not provided"
---

# 0004 — Identify checkouts with a local Git UUID

- **Status:** Accepted
- **Date:** 2026-11-06
- **Deciders:** Tech Lead and Plugin user

## Context

The policy stores paths to selected repositories, but a path can be replaced by a different checkout or the original checkout can move. A path or repository name alone cannot prove that a saved target still identifies the same local checkout. The policy does not inspect remotes or remote permissions.

## Decision drivers

- The spec requires invalid or replaced paths to stop for explicit reselection rather than silently substituting another repository.
- Repository identity must be local and must not depend on remote URLs or permissions.
- Branch creation and identity recording both require local write access and must fail visibly when unavailable.

## Considered options

1. **Local Git UUID** — write a random checkout identifier to that repository's `.git/config` and record it with the canonical path in policy state.
2. **Git metadata marker file** — store the checkout UUID in a dedicated file under the checkout's Git metadata directory and record it with the canonical path in policy state.

## Decision outcome

**Chosen:** Assign each selected checkout a random local UUID stored in its Git configuration, and store the UUID with its canonical path in `.sdd/branch-policy.json`. If the saved path is missing or the UUID does not match, stop and require explicit reselection; never locate or substitute a repository by name.

The dedicated marker-file option could provide the same identity property, but adds a new private metadata-file format and path convention without improving portability or failure handling over Git's existing local configuration.

## Consequences

**Positive**
- Detects a different checkout substituted at a previously saved path.
- The UUID remains with the Git metadata if a checkout moves, allowing an explicit reselection to confirm its identity.
- No remote information is read or changed.

**Negative**
- Initial selection modifies local `.git/config`; a read-only Git directory prevents setup.
- A fresh clone has a different local configuration and must be explicitly selected and assigned an identifier.

**Neutral**
- Linked worktrees and submodules remain excluded from selection, so the identifier is written only to eligible independent checkouts.

## Links

- Spec: [[../spec.md]]
- SAD: [[../sad.md]] §4
- Related ADR: [[0003-store-policy-in-an-ignored-project-json-file]]
