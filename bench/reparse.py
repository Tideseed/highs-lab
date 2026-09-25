#!/usr/bin/env python3
"""Re-parse the kept solver logs of a result directory into its JSON records (e.g. to add trajectories to results
recorded before the parser knew about them). Only log-derived fields are updated. reparse.py <result-dir>..."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run import parse_log  # noqa: E402

for d in map(Path, sys.argv[1:]):
    n = 0
    for p in d.glob("*.json"):
        if p.name.startswith("RESOURCES") or p.name.endswith(".stale.json"):
            continue
        log = d / "work" / p.stem / "stdout.txt"
        if not log.exists():
            continue
        rec = json.loads(p.read_text())
        rec.update(parse_log(log.read_text()))
        p.write_text(json.dumps(rec, indent=1))
        n += 1
    print(d, n, "records re-parsed")
