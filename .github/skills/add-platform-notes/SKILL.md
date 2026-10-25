---
name: add-platform-notes
description: When touching a camera body, update NOTES/PITFALLS and docs pointers.
---

1. Identify the install family first (`ADRs/001-two-install-families.md`):
   - Classic → `src/ml/platforms/<PLATFORM>/`
   - Film-in-ML → `integrations/magiclantern/<PLATFORM>/`

2. **Classic checklist**
   - Update or add platform README / comments for holes, vendor AUTOEXEC path, `patch.json`.
   - Never point Film-in-ML docs at `patch-film.py` as the ship path for DryOS bodies.
   - 40D stays experimental until `holes_confirmed` and FIO are proven.

3. **Film-in-ML checklist**
   - Update `integrations/magiclantern/<PLATFORM>/NOTES.md` (boot object, FW, build command).
   - Keep `SOUP-PIN.txt` accurate if the ML pin changes; mention it in the PR.
   - Do **not** run `patch-film.py`. For 50D memory/FIO/GUI ideas, read
     `src/ml/platforms/50D.109/PITFALLS.md` and `ADRs/002-50d-film-in-ml-only.md`.

4. **Shared docs**
   - If the platform matrix or build command changed: update `docs/system/platforms.md`
     and `.github/copilot-instructions.md` platform table.
   - If behaviour/invariants changed: update the matching `docs/features/*/overview.md`.

5. Do not invent firmware versions outside the supported table in
   `.github/copilot-instructions.md`.
