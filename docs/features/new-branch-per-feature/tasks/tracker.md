# Tracker — new-branch-per-feature

> Status of every task in the epic. `implement` updates **Status** and **Step** after every
> subagent it runs (and commits them with the task), so this table shows where the run is right now.
> Status: `todo` · `in_progress` · `blocked` · `review` · `done`.
> Step: `SELECT` · `RED` · `GREEN` · `REFACTOR` · `GATE` · `REVIEW` · `COMMIT` (`-` before the task starts).
> A `blocked` row carries its reason in Step, e.g. `GATE - lint red after 3 retries`.

| # | Task | Layer | Owner | Estimate | Blocked by | Status | Step |
|---|---|---|---|---|---|---|---|
| T1 | Define local policy state and active-feature resolution | app | Tech Lead | 6h | - | todo | - |
| T2 | Discover and explicitly select eligible repositories | app | Tech Lead | 6h | T1 | todo | - |
| T3 | Enforce safe branch-setup preflight | app | Tech Lead | 6h | T2 | todo | - |
| T4 | Record checkout identity and verify local write access | app | Tech Lead | 4h | T3 | todo | - |
| T5 | Create feature branches and resume pending setup | app | Tech Lead | 6h | T4 | todo | - |
| T6 | Enforce the shared branch gate at every write boundary | app | Tech Lead | 6h | T1, T5 | todo | - |
| T7 | Wire the first 12 registered skills to the branch gate | wiring | Tech Lead | 8h | T6 | todo | - |
| T8 | Wire the remaining 11 registered skills to the branch gate | wiring | Tech Lead | 8h | T6 | todo | - |
| T9 | Validate branch-gate coverage in CI | tests | Tech Lead | 4h | T7, T8 | todo | - |
| T10 | Document host-hook information as non-enforcing | docs | Tech Lead | 3h | T6 | todo | - |
| T11 | Add safe-setup acceptance evaluation scenarios | tests | Tech Lead | 6h | T5 | todo | - |
| T12 | Add active-gate and performance evaluation scenarios | tests | Tech Lead | 8h | T6, T9, T10, T11 | todo | - |

**Total:** 12 tasks, ~9 person-days.
