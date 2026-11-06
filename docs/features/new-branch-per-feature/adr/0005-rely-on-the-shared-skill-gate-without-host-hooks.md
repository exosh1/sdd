---
status: Accepted
owner: "Tech Lead"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-06"
feature_size: "M"
ticket: "Not provided"
---

# 0005 — Rely on the shared skill gate without host hooks

- **Status:** Accepted
- **Date:** 2026-11-06
- **Deciders:** Tech Lead and Plugin user

## Context

Host platforms offer different hook locations, trust requirements, execution environments, and blocking behavior. The user chose not to add separate executable branch checks for each host, to keep one canonical policy procedure.

## Decision drivers

- The shared gate must be the only required branch-policy check regardless of host hook availability.
- Host adapters differ, and a second implementation of repository and branch checks could drift from the shared skill policy.
- Host hook capabilities may be mentioned as informational context but must not be presented as branch-policy enforcement.

## Considered options

1. **No shipped branch-check hooks** — require the same shared skill gate in every SDD skill and document host capabilities and limitations.
2. **Supplementary host-specific hooks** — implement separate blocking Git checks for hosts that can scope them to SDD actions.

## Decision outcome

**Chosen:** Do not ship or rely on host-level branch-check hooks. The shared skill gate is the only required check; host hook capabilities may be documented as informational context without implying they enforce this policy.

## Consequences

**Positive**
- Keeps one branch-check procedure instead of duplicating state parsing and Git logic across host-specific scripts.
- Avoids installing or trusting executable hooks as a prerequisite for using the policy.

**Negative**
- Skill instructions cannot block arbitrary direct writes or guarantee that a host follows every step.
- Direct operations outside SDD skills are not blocked by this policy.

**Neutral**
- Host hook capabilities are outside this feature's enforcement contract and may be reconsidered later without changing the branch-policy state format or shared skill gate.

## Links

- Spec: [[../spec.md]]
- SAD: [[../sad.md]] §4
- Related ADR: [[0002-use-shared-instructions-for-branch-checks]]
- Claude Code hooks: https://code.claude.com/docs/en/hooks
- Codex hooks: https://developers.openai.com/codex/hooks
- Cursor hooks: https://cursor.com/docs/hooks
- Copilot hooks: https://docs.github.com/en/copilot/reference/hooks-reference
