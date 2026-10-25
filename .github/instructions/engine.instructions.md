---
applyTo: "src/engine/**"
---

# Look engine (`src/engine`)

Shared freestanding C99 look pipeline for camera and desktop. Same sources
build into Classic `SE.BIN`, Film-in-ML, and host `filmdev`.

## Rules

- Integer-only on every per-pixel path. No floating point on those paths.
- No libc on camera builds; keep the engine freestanding-friendly.
- Do not split host-only helpers into files that camera targets compile
  unless they stay freestanding-safe.
- Stock format and CR2/JPEG paths live here; film definitions are plain
  text under `src/stocks/` (not under `engine/`).
- After substantive engine edits: `make -C src test` and `make -C src arm`.

## Pointers

- Overview: `docs/features/look-engine/overview.md`
- Host driver: `src/host/`
- Stock format notes: `src/stocks/README.md`
