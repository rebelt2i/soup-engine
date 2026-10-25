---
applyTo: "src/ml/**"
---

# Classic path (`src/ml`)

VxWorks Classic bodies only: freestanding `SE.BIN` (`soupeng.bin`) plus a
binary-patched Magic Lantern `AUTOEXEC.BIN` via `patch-film.py`.

## Platforms under this tree

| Dir | Status |
|-----|--------|
| `platforms/5DC.111/` | Released Classic |
| `platforms/40D.111/` | Experimental — see that README |
| `platforms/50D.109/` | **Pitfalls archive only** — shipping path is Film-in-ML |

## Rules

- Per-body contract: `cam.h`, `mlmap.h`, `payload.ld`, `mlstub.S`, `patch.json`.
- Build: `make -C src payload PLATFORM=5DC.111` (runs payload + `patch-film.py`).
- CI rebuilds `SE.BIN` from source; re-patching still needs vendor stock
  `autoexec.bin` under `src/vendor/magiclantern-5Dc/` (not shipped).
- `PLATFORM` in Makefiles may default to `50D.109` for host convenience —
  **pass `PLATFORM=5DC.111` (or `40D.111`) explicitly** for Classic work.
- Do not add Film-in-ML / DryOS boot assumptions here. Film-in-ML lives under
  `integrations/magiclantern/`.

## Pointers

- Feature overview: `docs/features/classic/overview.md`
- ADR: `ADRs/001-two-install-families.md`
- 50D abandoned SE path: `platforms/50D.109/PITFALLS.md`, `ADRs/002-50d-film-in-ml-only.md`
