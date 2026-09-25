#!/usr/bin/env python3
"""Create a codebase-map note: new-candidate.py ID "Title" area "where" "what" "fix" effort gate [verified]"""
import sys
from pathlib import Path
cid, title, area, where, what, fix, eff, gate = sys.argv[1:9]
ver = len(sys.argv) > 9 and sys.argv[9] == "verified"
d = Path(__file__).resolve().parents[1] / "vault/40-codebase-map"
p = d / f"{cid} {title.replace('/', ' and ')}.md"
p.write_text(f"""---
id: {cid}
area: {area}
status: candidate
gate: {gate}
effort: {eff}
verified_in_source: {str(ver).lower()}
profiled_share: null
branch: null
---
# {cid}: {title}

**Where:** {where}

**What:** {what}

**Proposed fix:** {fix}

**Source:** static read of `latest` on 2026-09-25{' (checked by hand)' if ver else ' (sweep agent, not yet checked by hand)'}.
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
""")
print(p.name)
