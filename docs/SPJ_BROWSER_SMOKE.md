# SPJ Chromium smoke test (manual only)

This optional workflow executes the actual static HTML form in headless Chromium. It checks noindex, KKPD and marketplace review prompts, the 1 October 2026 boundary, HTML required validation, and absence of tax totals.

Run manually via GitHub Actions > SPJ Browser Smoke (Manual) > Run workflow. It is **not** included in CI Light to preserve minutes and download budget. Playwright is installed only for the manual run; no dependency files are committed.

Browser smoke is not a legal review, and no publication or tax computation is authorized. Status: PRE_RELEASE / HOLD.
