---
name: highs-upstream-issue
description: Draft a GitHub issue to ERGO-Code/HiGHS from a gated lab result, following HiGHS's AI-contribution policy and the per-post approval rule. Use when a lab branch passed the gate, when asked to report a HiGHS finding upstream, or to add evidence to an existing HiGHS issue.
---
# Report a finding upstream

1. **Policy:** HiGHS does not accept AI-generated PRs to its solvers (CONTRIBUTING.md). **Never open a PR.** Write an issue that describes the problem, the evidence and the idea, and link the fork branch diff (`https://github.com/Tideseed/HiGHS/compare/latest...lab/<idea>`) as an illustration. The HiGHS developers decide how to implement it.
2. **Prior art:** `gh issue list -R ERGO-Code/HiGHS --state all --search "<keywords>"` with several phrasings, and `gh pr list` too. Link related issues. If one already covers it, draft a comment instead of a new issue.
3. **Draft** in `vault/70-upstream/DRAFT <title>.md`:
   - the attribution line: an AI agent (Claude Code) filing on behalf of Berk Orbay (@berkorbay), who asked for it
   - what is slow and where (file:line on `latest` at a named SHA)
   - the measurement: arms, instance set, seeds, the gate numbers with CI, the machine, and whether the search is identical
   - the minimal idea
   - what we did not check

   Keep it short and factual. No marketing, and don't overstate generality.
4. **Show the draft to Berk and wait for an explicit yes for this post.** Permission is per post, never standing.
5. **After filing:**
   - rename the note to `FILED #<n> <title>.md` and add the URL
   - update the candidate note's log
   - add the issue to optopt's `vault/70-upstream/` index if it relates to that paper
