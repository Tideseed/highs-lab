# D-002: Build and benchmark windows (2026-09-25)

The host runs two local LLM servers holding ~79 GB of the 121 GiB unified memory; its operator rule allows compiles
only with >30 GB free, inside a 12 GiB / 600 % CPU systemd scope.
**Decision (Berk):** on 2026-09-25 both local agents may be taken down for the lab window. Afterwards: if the agents
are busy, apply the strict rule (skip the build) and notify; when they are idle, they may be stopped for a build and
restored.
Clean benchmark measurements always run with the LLM servers stopped; smoke runs may run beside them.
