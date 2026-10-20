# Cloudflare Pages Deployment

Production site: https://asnpemda.pages.dev  
Source repository: https://github.com/wiztechid/asnpemda  
Production branch: `main`

## Public build boundary
Cloudflare Pages runs `python scripts/build_site.py` and publishes `dist/`. The builder starts from an empty output directory and copies only an explicit public allowlist. It never copies the repository root. Editorial documents, source registries, research notes, scripts, schemas, candidate records, and unapproved drafts stay outside the Pages artifact.

An article enters `dist/` and `sitemap.xml` only when its JSON record is explicitly approved, has `publicationState: PUBLISHED`, has a valid slug, exists as an HTML page, and is not marked noindex.

## Release controls
- CI light runs source/link checks and the allowlist build smoke test.
- Heavy validation is manual via workflow dispatch after a substantive batch.
- A successful build or deployment does not change the editorial release state.
- The site remains PRE_RELEASE / HOLD until the publication gates and a separate human GO decision are complete.
