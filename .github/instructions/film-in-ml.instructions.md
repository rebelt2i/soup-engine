---
applyTo: "integrations/magiclantern/**"
---

# Film-in-ML (`integrations/magiclantern`)

DryOS bodies boot a **rebuilt** Magic Lantern `autoexec.bin` with the Film
menu. They do **not** boot `SE.BIN`.

## Layout

- `_common/` — shared Film page / develop sources
- `<PLATFORM>/` — Makefile, `soup_cam.h`, `NOTES.md`, `SOUP-PIN.txt`
- Platforms: `50D.109`, `6D.116`, `5D3.123`

## Rules

- Build only via `python3 src/tools/build-ml.py --platform <PLATFORM>`.
- **Never** run `src/tools/patch-film.py` on these bodies.
- Honour `SOUP-PIN.txt` (do not casually retarget ML without updating pin + docs).
- Overlay order: `_common` then platform directory.
- Boot objects differ: 50D/5D3 `boot-d45.o`; 6D `boot-d45-am.o` — do not
  copy 50D boot assumptions onto 6D.
- 5D Mark III: firmware **1.2.3 only**.
- Before changing memory / FIO / GUI assumptions on 50D, read
  `src/ml/platforms/50D.109/PITFALLS.md` and `ADRs/002-50d-film-in-ml-only.md`.

## Pointers

- Feature overview: `docs/features/film-in-ml/overview.md`
- Per-body: `integrations/magiclantern/<PLATFORM>/NOTES.md`
- Build guide: `docs/guides/build-from-source.md`
