# Feature: look engine

Last reviewed: 2026-10

## What it is

The shared grading core in `src/engine/`: stock `.fs` parsing, CR2 read,
look/grade, JPEG write. Freestanding C99, integer per-pixel paths, no libc
on camera builds. **Same sources** drive Classic `SE.BIN`, Film-in-ML, and
desktop `filmdev` (`src/host/`).

## Why it exists

One look definition → every supported body and the host tools, without a
second “desktop grade” codebase.

## Invariants

- Integer-only on per-pixel paths.
- Film looks are plain-text stocks under `src/stocks/` (see that README).
- Host gate without samples: `make -C src test` (`filmdev selftest` +
  `out/lookcheck`). ARM freestanding smoke: `make -C src arm`.
- Byte-exact camera/desktop contract (when samples exist): `make -C src simtest`.

## Related

- Scoped AI rules: `.github/instructions/engine.instructions.md`
- Architecture: `docs/system/architecture.md`
