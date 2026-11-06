---
status: Accepted
owner: "Tech Lead"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-06"
feature_size: "M"
ticket: "Not provided"
---

# 0003 — Store policy in an ignored project JSON file

- **Status:** Accepted
- **Date:** 2026-11-06
- **Deciders:** Tech Lead and Plugin user

## Context

The policy must remember each feature's opt-in and repository selection, plus the explicitly active feature, across branch changes. It must remain local to the project and readable by different AI hosts. Feature documents themselves are branch-specific, and the existing `.claude/sdd.local.md` is a host-named settings file with a separate ownership convention.

## Decision drivers

- The spec requires state to remain readable from any branch and to stay in local project state.
- The selected repositories and active feature must be available to every skill gate.
- The repository supports Git-ignored local settings but has no runtime datastore.

## Considered options

1. **`.sdd/branch-policy.json`** — store project-wide policy state in an ignored, host-neutral JSON file.
2. **Local Git configuration** — store all policy and active-feature records in `.git/config`.
3. **`.claude/sdd.local.md`** — add feature policy state to the existing settings file.

## Decision outcome

**Chosen:** `.sdd/branch-policy.json` at the root of the repository containing the feature documents, with that exact file ignored by a local `.git/info/exclude` entry in that checkout. It records per-feature opt-in and repository selection, the explicit active feature, and setup status (`pending` until every selected repository is on its target branch, then `active`); it is local, branch-independent, and not coupled to a host's settings format. Pending state lets setup resume safely after partial branch creation. The local exclude avoids a tracked `.gitignore` edit that would make the required clean-base branch preflight fail or make setup retries dirty.

## Consequences

**Positive**
- One structured, host-neutral source of truth supports multiple features and selected repositories.
- Branch changes do not replace the ignored state file.
- Git-local configuration remains available for a per-checkout identity marker without crowding the policy record.

**Negative**
- An absent policy file means no feature has opted in and preserves the legacy workflow; once an opted-in policy is expected, missing, malformed, or unreadable JSON must fail closed.
- A new state file schema needs validation and migration rules if its format changes.

**Neutral**
- The mandatory repository containing the feature documents is the anchor for discovering the policy file; selected repository paths are stored explicitly.

## Links

- Spec: [[../spec.md]]
- SAD: [[../sad.md]] §4
- Related ADR: [[0004-identify-checkouts-with-a-local-git-uuid]]
