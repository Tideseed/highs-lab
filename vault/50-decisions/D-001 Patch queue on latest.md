# D-001: Patch queue on top of upstream `latest` (2026-09-25)

**Decision:** every improvement is a single-purpose `lab/<idea>` branch cut from upstream `latest` and rebased daily;
`dev-tideseed` is regenerated as `latest` + accepted branches. Three arms are always compared: `main`, `dev`,
`dev-tideseed`.
**Why:** Berk: "latest improvements are important and building on top of them is even more important". A patch queue
keeps each branch's diff against `latest` minimal, which is what an upstream issue links to, and makes overlap with
upstream work visible as a conflict or an empty diff.
**Consequence:** conflicts are resolved automatically (Berk, same day) with gates; see [[Sync and auto-resolution]].
