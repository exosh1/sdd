---
status: Draft
owner: "Plugin user"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-06"
feature_size: "M"
---

# Spec — new-branch-per-feature

> **Glossary:** [CONTEXT](./CONTEXT.md) (feature-scoped; `Plugin user` reuses the role in `docs/architecture-map.md`).
> **Reference module / docs / channels used:** `skills/_shared/settings-file.md`, `skills/_shared/agent-roster.md`, `skills/_shared/tool-adapters.md`, `skills/_shared/write-and-commit.md`, `skills/implement/SKILL.md`, `skills/implement/references/inputs.md`, `skills/config/references/interview.md`, `README.md`, `install.sh`; official host documentation: [Claude Code hooks](https://code.claude.com/docs/en/hooks), [Codex hooks](https://developers.openai.com/codex/hooks), [Cursor hooks](https://cursor.com/docs/hooks), and [Copilot hooks](https://docs.github.com/en/copilot/reference/hooks-reference).

## 1. Context

SDD plugin users need each feature's planning and implementation work isolated from unrelated changes. Today, the `feature` branch strategy is read by `implement` only and creates a branch only when the current branch is the repository's default; document stages commit on the current branch. The plugin does not have one feature-scoped rule covering all skills or multiple repositories.

This gap matters in projects whose modules are separate Git repositories: a feature can otherwise leave its documents or code on a default or unrelated branch in one of those repositories. Project-wide SDD skills also need a way to identify which feature's branch policy they must enforce.

The chosen direction is an opt-in `new_branch_per_feature` policy that is saved per feature in local project state independent of the currently checked-out branch, selects eligible repositories explicitly, and applies one shared branch check to every SDD skill before stage writes, and again before feature writes and commits. The shared gate must be able to read that state before feature work on any branch. The policy does not install or rely on host-level enforcement; documentation may describe host hook capabilities as informational context only.

Owner-confirmed constraints: the active branch name is exactly the feature slug, without a prefix. Branch setup is local to each checkout; the policy does not inspect or change remote branches or permissions. Branch setup is allowed only from a clean current branch whose name begins with the case-sensitive literal prefix `main`, `master`, `develop`, or `release`, or whose name exactly matches the default branch recorded in that checkout. The feature branch is created from that current branch; being on another branch does not authorize creating it from the default branch. Unsafe state, a non-active existing local target branch, or a branch mismatch stops the stage without automatic switching, stashing, resetting, or deleting. A dirty tree is allowed after the target branch is already active. Discovery stays within the project workspace unless the owner explicitly selects another path. The read-only branch discovery/check operation uses the low-cost search/read model; other stage and judgment models remain unchanged.

## 2. Goals

- Isolate opted-in feature work on the feature's exact slug branch across all selected repositories and all SDD skills.
- Prevent a stage from writing or committing feature work when any selected repository fails the branch preflight, and explain the specific repository and recovery action.
- Preserve the existing workflow for features that have not opted into the new policy.

## 3. Non-goals

- Replacing or globally changing the existing `branch_strategy` setting; it remains the legacy `implement` behavior for features that do not opt in.
- Creating separate branches for ordinary directories or modules that are not independent Git repositories; they remain covered by their containing repository's branch.
- Automatically checking out a pre-existing feature branch, stashing or committing user changes, resetting or deleting branches, or rolling back a branch already created in another repository; these actions can disturb user work.
- Enforcing the new policy in projects or features that have not opted in; opt-in avoids changing established workflows unexpectedly.

## 4. User stories

### US-01: Enabling feature isolation

**As a** Plugin user
**I want** to opt a feature into its own branch policy
**So that** its planning and implementation work stays separate from other work

### US-02: Selecting project repositories

**As a** Plugin user
**I want** to choose which independent repositories participate in a feature
**So that** unrelated repositories remain untouched

### US-03: Preparing branches safely

**As a** Plugin user
**I want** branch setup to stop when a repository is not in an approved state
**So that** existing work and branches are not silently disturbed

### US-04: Verifying every feature stage

**As a** Plugin user
**I want** every SDD skill to check the feature branch across all selected repositories
**So that** no stage writes or commits feature work on the wrong branch

### US-05: Associating utility skills

**As a** Plugin user
**I want** project-wide SDD skills to resolve an unambiguous active feature
**So that** those skills follow the same branch policy as feature-specific stages

## 5. Acceptance criteria

### AC-01 (US-01) — happy

**Given** a Plugin user starts a feature with `new_branch_per_feature` and completes repository selection
**When** the first feature stage initializes the policy
**Then** the plugin creates any missing local branch named exactly for the feature slug without checking it out, saves the policy and selection in local project state that remains readable from any branch with setup marked `pending`, and leaves unselected repositories unchanged; the Plugin user must activate the target branch manually in every selected repository, and no feature-stage work starts until all selected repositories are on that branch and setup is marked `active`

### AC-02 (US-02) — happy

**Given** a Plugin user enables the policy in a project workspace
**When** the plugin recursively discovers independent Git checkouts within that workspace or validates paths explicitly provided by the user
**Then** it excludes submodules and linked worktrees from eligible repositories, and the user can explicitly choose repositories using checkboxes or a numbered text fallback; the repository containing the feature's SDD documents is mandatory, and no other repository is chosen implicitly

### AC-03 (US-03) — error

**Given** branch setup is needed and a selected repository has any of these unsafe states: tracked changes (staged or unstaged), untracked non-ignored files, a current branch that is neither an allowed base nor the locally recorded default branch, or an existing feature branch that is not active
**When** the user starts an SDD stage
**Then** the stage stops before feature work, reports the affected repository and reason, and does not automatically switch to an existing branch, stash, reset, or remove work

### AC-04 (US-03) — authorization

**Given** the Plugin user lacks local write permission for required policy-state, checkout-identity, or branch setup writes in a selected repository
**When** the plugin initializes or resumes the feature policy
**Then** it stops before writing feature artifacts, reports the result for every selected repository, and preserves any branches already created

### AC-05 (US-04) — domain invariant

**Given** a feature has an opted-in branch policy with setup marked `active`
**When** an SDD skill is about to perform a stage write, feature write, or feature commit and a selected repository's active branch does not exactly match the feature slug
**Then** the skill blocks the affected stage writes and commits and reports the mismatch before the affected write or commit; read-only work and explicit recovery actions remain available

### AC-06 (US-04) — cross-context

**Given** a feature spans multiple selected repositories and setup is marked `active`
**When** any one repository fails a branch check before a stage write, feature write, or feature commit
**Then** feature writes and commits for the stage are blocked, even if the repository from which it was launched has the correct branch

### AC-07 (US-05) — error

**Given** an SDD skill is invoked without a feature slug while branch policies are in use (a project-wide invocation)
**When** local project state marks exactly one feature as active, or marks none or multiple features as active
**Then** the skill uses the one explicitly active feature or requests an explicit feature slug, respectively, and does not proceed with feature writes or commits while the feature remains ambiguous. An active feature is one explicitly selected as active in local project state; it remains active until the user changes that selection

### AC-08 (US-02) — error

**Given** a saved repository path is missing, no longer identifies the same repository, or identifies only an ordinary directory
**When** a feature stage checks its saved selection
**Then** the stage stops and asks the Plugin user to choose a valid repository again rather than silently substituting its parent or another repository

### AC-09 (US-03) — error

**Given** all selected repositories pass setup preflight but branch creation fails partway through
**When** the plugin reports the failure
**Then** it lists the state of each selected repository, leaves already-created branches intact, and performs no feature-stage work; a later run resumes setup only after every selected repository passes preflight. If a previously created feature branch is not active, the user must activate it manually before retrying; the plugin never resumes by switching branches

### AC-10 (US-04) — happy

**Given** a feature branch policy has completed setup and the current host does not provide an active blocking hook
**When** an SDD skill is about to perform a stage write, feature write, or feature commit
**Then** the shared branch gate verifies the saved policy and blocks writes and commits on mismatches, while read-only work and explicit recovery actions remain available; the policy does not install or rely on host hooks, and any host-specific hook information is informational only

### AC-11 (US-01) — happy

**Given** a feature has not opted into `new_branch_per_feature`
**When** the Plugin user runs an SDD skill
**Then** the existing workflow, including the legacy `branch_strategy` behavior, remains unchanged

### AC-12 (US-03) — domain invariant

**Given** a selected repository needs a new feature branch
**When** the plugin checks the current branch as the base
**Then** it accepts a current branch whose name begins with the case-sensitive literal prefix `main`, `master`, `develop`, or `release`; otherwise it accepts only an exact match for the default branch recorded in that checkout, and stops if neither condition holds

## 6. Non-functional requirements

| Aspect | Target | Measurement |
|---|---|---|
| Branch preflight latency | p95 ≤ 2 seconds per selected repository; branch creation and owner interaction excluded | Time 30 preflight runs against local fixtures containing 1, 3, and 10 repositories |
| Unsafe-state enforcement | 100% of branch mismatch, dirty setup, missing-repository, and branch-collision cases block before feature writes or commits | Manual host-driven acceptance matrix using disposable local Git repositories in each supported host |
| Skill coverage | 100% of registered SDD skills resolve and invoke the shared gate when a feature policy applies | CI validator checks every registered skill entrypoint |

If repository discovery needs an agent, it uses the existing Haiku search/read role; the branch-state check itself is deterministic and does not dispatch a judgment agent. This does not change the model used for other SDD stages or judgment agents.

## 6.1 Security / privacy

- **Data classification:** Internal — repository locations and branch names are project metadata and remain in the local workspace.
- **Personal data touched:** None.
- **AuthZ/AuthN impact:** No new identity or permission system; local branch creation uses the invoking user's local filesystem permissions and fails visibly when denied. Remote branch state and permissions are not checked.
- **Abuse cases:**
  - An invalid or replaced repository path: reject it and ask the owner to reselect rather than fall back to a parent or similarly named repository.
  - A path or slug that could be interpreted as a command or escape the intended workspace: validate it as data and reject it before any Git operation. The intended path set is the project workspace plus canonical Git roots the user explicitly selects, including roots outside the workspace; reject other external paths.
  - A user assumes host hooks provide branch-policy enforcement: make clear that the shared skill gate is the only required check and that host hook information is informational only.
  - A repository where branch creation is not authorized: report the failure and preserve any existing repository state.
- **Security review:** Required — this M feature adds cross-stage gates that can block repository operations.

## 7. Metrics / KPIs

- **Universal branch-policy coverage** — baseline: 0 of 23 skills apply the same feature-scoped, multi-repository branch guard; target: all 23 current skills invoke it before feature work, with new skills checked by CI, before release.
- **Successful feature setup** — baseline: no feature-scoped multi-repository setup; target: 100% of successful setup scenarios leave every selected repository on the exact feature-slug branch and preserve unselected repositories, before release.
- **Safe failure behavior** — baseline: no shared branch-policy failure matrix; target: 100% of defined unsafe-state scenarios stop before feature writes or commits, with no unintended branch changes, before release.

## 8. Resolved decisions

- Checkout identity uses a local Git UUID; see ADR-0004.
- The shared skill gate is the only required branch-policy check. Host hook capabilities may be documented as informational context, but the policy does not install or rely on hooks; see ADR-0005.
