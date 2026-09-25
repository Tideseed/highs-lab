---
id: P3
area: io
status: candidate
gate: identical model
effort: 1 d
verified_in_source: false
profiled_share: null
branch: null
---
# P3: MPS parser per-token strings

**Where:** highs/io/HMpsFF.cpp:399-489, 731, 903, 2101

**What:** Keyword test with toupper per line, ~6 temp strings and 3 hash lookups per nonzero, locale atof.

**Proposed fix:** string_view tokenizer, from_chars, one lookup.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
- 2026-09-25: evidence — neos-3402454-bohle cannot even be parsed within 20 s ("Parser reached timeout", both dev and branches).
