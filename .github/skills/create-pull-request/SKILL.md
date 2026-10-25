---
name: create-pull-request
description: Open a PR using this repo’s template and platform/test checklist.
---

1. Prefer short imperative commit subjects (e.g. “Add 6D Film-in-ML notes”).
2. Fill the PR body from `.github/PULL_REQUEST_TEMPLATE.md` — do not invent a different structure.
3. Mark every platform you actually touched; if only docs/host, check “None”.
4. Paste the exact test commands you ran. Minimum for engine or shared C: `make -C src test` and usually `make -C src arm`.
5. If Classic changed: note `PLATFORM=5DC.111` (or `40D.111`) payload/patch status.
6. If Film-in-ML changed: note `build-ml.py --platform …` and that `patch-film.py` was **not** used.
7. Link any ADR or `docs/` updates. If you settled a new architectural choice, add or update an ADR instead of burying it in the PR only.
8. Default branch is `master` (workflows also accept `main`).
