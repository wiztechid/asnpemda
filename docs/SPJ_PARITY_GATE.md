# SPJ Prototype Parity Gate

CI Light now runs static checks for required SPJ form fields, ISO date-validation markers, integer-rupiah validation, KKPD and marketplace review prompts, noindex status, and absence of network submission or unsafe HTML injection. The tax decision test suite additionally rejects malformed matrix rule IDs, including unhashable JSON values.

These are **static safety checks**, not browser execution tests or legal approval. The JavaScript form and Python decision engine remain separate implementations. Full behavior parity, up-to-date legal citations, and explicit human publication approval remain release blockers.

**Status: PRE_RELEASE / HOLD.** No automatic tax computation.
