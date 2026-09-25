---
id: P1
area: presolve
status: profiled
gate: identical
effort: 0.5-1 d
verified_in_source: true
profiled_share: 17.5% toguru
branch: null
---
# P1: markChangedCol walks whole column

**Where:** highs/presolve/HPresolve.cpp:653-660; reader dualFixing :5495

**What:** Every unlink/addToMatrix/transformColumn walks the full column to clear singleEquationChecked, even if the column is already flagged; quadratic on dense columns during substitution.

**Proposed fix:** Lazy epoch stamps compared in dualFixing. Developers active in dual fixing (#3244): coordinate.

**Source:** static read of `latest` on 2026-09-25 (checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
