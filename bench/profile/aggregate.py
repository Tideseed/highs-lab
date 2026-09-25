#!/usr/bin/env python3
"""Aggregate a sweep.sh output dir: mean self% per symbol across instances (each instance weighted equally),
plus the top symbol per instance. aggregate.py <dir> [--incl] [--top 30]"""
import re, sys, collections
from pathlib import Path
d = Path(sys.argv[1]); incl = "--incl" in sys.argv
top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 30
suffix = ".incl.txt" if incl else ".self.txt"
agg = collections.defaultdict(float); per = {}
files = sorted(d.glob("*" + suffix))
for f in files:
    rows = []
    for line in f.read_text().splitlines():
        m = re.match(r"\s+([\d.]+)%\s+(?:([\d.]+)%\s+)?\[\.\]\s+(.*?)\s{2,}", line) or re.match(r"\s+([\d.]+)%\s+(?:([\d.]+)%\s+)?\[\.\]\s+(.*)", line)
        if not m: continue
        sym = re.sub(r"\(.*", "", m.group(3)).strip()
        rows.append((float(m.group(1)), sym))
    seen = set()
    for pct, sym in rows:
        if sym in seen: continue
        seen.add(sym); agg[sym] += pct / len(files)
    per[f.name.replace(suffix, "")] = rows[:3]
print(f"{len(files)} instances, mean {'inclusive' if incl else 'self'} %")
for sym, pct in sorted(agg.items(), key=lambda x: -x[1])[:top]:
    print(f"{pct:6.2f}  {sym[:110]}")
print()
for k, rows in per.items():
    print(f"{k:28} " + " | ".join(f"{p:.0f}% {s[:45]}" for p, s in rows))
