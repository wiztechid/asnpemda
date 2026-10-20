# Release decision v0.9

Status: HOLD / PRE_RELEASE.

The public site shell is served by Cloudflare Pages from an allowlisted `dist/` artifact. Unapproved article drafts, prototypes, editorial documents, data, source registries, and research files are excluded from the deployment artifact.

This task improves site structure and publication boundaries. It does not approve a policy article or authorize an editorial launch.

Open gates:
- Evidence-backed launch article and exact-revision human approval.
- Public correction/contact route.
- Final mobile/accessibility/SEO QC on the publication corpus.
- Separate human GO decision.

A passing CI, build, or deployment does not override these gates.
