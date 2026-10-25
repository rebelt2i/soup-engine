# Add or port a body

Last reviewed: 2026-10

High-level only. Read existing NOTES / PITFALLS before copying patterns
across families.

## 1. Choose the family

| If the body is… | Join |
|-----------------|------|
| VxWorks Classic (Digic II/III style, SE payload) | **Classic** — `src/ml/platforms/<PLATFORM>/` |
| DryOS with ML Film menu | **Film-in-ML** — `integrations/magiclantern/<PLATFORM>/` |

Do not invent a hybrid boot. See [ADR 001](../../ADRs/001-two-install-families.md).
50D-class DryOS: do not start from heap `SE.BIN` —
[ADR 002](../../ADRs/002-50d-film-in-ml-only.md).

## 2. Classic sketch

1. Add `src/ml/platforms/<PLATFORM>/` (`cam.h`, `mlmap.h`, `payload.ld`,
   `mlstub.S`, `patch.json`).
2. Vendor stock AUTOEXEC under `src/vendor/…` (not shipped in git as a
   redistributable if ML forbids it — follow existing 5DC/40D practice).
3. Prove FIO and holes before marking `holes_confirmed`.
4. Wire `make payload PLATFORM=…` and document in `docs/system/platforms.md`.

## 3. Film-in-ML sketch

1. Copy a close sibling under `integrations/magiclantern/` (e.g. 50D → new Digic 4/5).
2. Set boot object, playback sizes in `soup_cam.h`, Makefile, `SOUP-PIN.txt`, `NOTES.md`.
3. Build with `python3 src/tools/build-ml.py --platform …` only.
4. Update platform tables in `.github/copilot-instructions.md` and
   `docs/system/platforms.md`; extend CI/release matrix when shipping.

## 4. Always

- Run `make -C src test` (and `arm` if engine/camera C changed).
- Follow `.github/skills/add-platform-notes/SKILL.md`.
- User-facing install rows belong in the root README when the body is released.
