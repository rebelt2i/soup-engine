# Feature: Film-in-ML

Last reviewed: 2026-10

## What it is

DryOS bodies (`50D.109`, `6D.116`, `5D3.123`, `550D.109`) boot a Magic Lantern
`autoexec.bin` **rebuilt** with Soup’s Film menu. Shared sources:
`integrations/magiclantern/_common/`. Per-camera: Makefile, `soup_cam.h`,
`NOTES.md`, `SOUP-PIN.txt`.

The camera does **not** load `SE.BIN`. Develop output is typically
`FLM_nnnn.JPG`; config may use `ML/SE.CFG`.

## Why it exists

Heap-loaded `SE.BIN` + GUI hook failed on 50D (malloc carve, FIO, clean-time
hooks). Film-in-ML is the shipping design for these bodies —
[ADR 002](../../../ADRs/002-50d-film-in-ml-only.md),
[`PITFALLS.md`](../../../src/ml/platforms/50D.109/PITFALLS.md).

## Invariants

- Build only with `python3 src/tools/build-ml.py --platform <PLATFORM>`.
- **Never** `patch-film.py` on these platforms.
- Honour `SOUP-PIN.txt` (pin historically `ed3e7c0d` / `2025_release_01`).
- Boot objects differ (6D uses `boot-d45-am.o`); do not copy 50D assumptions blindly.
- 5D3: firmware **1.2.3 only**.

## Build

```sh
python3 src/tools/build-ml.py --platform 50D.109
python3 src/tools/build-ml.py --platform 6D.116 --card /path/to/card
python3 src/tools/build-ml.py --platform 5D3.123 --card /path/to/card
python3 src/tools/build-ml.py --platform 550D.109 --card /path/to/card
```

## Related

- `.github/instructions/film-in-ml.instructions.md`
- Per-body `NOTES.md` under `integrations/magiclantern/<PLATFORM>/`
