---
id: O1
area: options
status: candidate
gate: full
effort: machine hours
verified_in_source: false
profiled_share: null
branch: null
---
# O1: Options off by default

**Where:** parallel=on (multi-worker tree search), mip_heuristic_run_zi_round, mip_heuristic_run_shifting, mip_heuristic_effort, simplex_strategy=3

**What:** Existing code paths that are off by default.

**Proposed fix:** Option sweep; no code.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
