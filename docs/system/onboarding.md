# Developer onboarding

Last reviewed: 2026-10

Photographers: skip this page — use the root [README](../../README.md) and a
release zip.

## Toolchain

- Python 3, `make`, host `cc`
- `arm-none-eabi-gcc` (camera / ARM smoke)
- `git` (Film-in-ML clones Magic Lantern)
- Windows: put Git’s `usr\bin` on `PATH` so ML makefiles find `sh`
- Optional: `ARM_BINPATH` = directory containing `arm-none-eabi-gcc`

## First safe change

1. Read [AGENTS.md](../../AGENTS.md) and [.github/copilot-instructions.md](../../.github/copilot-instructions.md).
2. Skim [architecture.md](architecture.md) and [platforms.md](platforms.md).
3. From the repo root:

   ```sh
   make -C src test
   make -C src arm
   ```

   No CR2 samples required for `test`.

4. Pick a family before touching camera code ([ADR 001](../../ADRs/001-two-install-families.md)).

## Layout cheat sheet

See [src/README.md](../../src/README.md). Film-in-ML overlays live under
`integrations/magiclantern/`, not under `src/ml/`.

## Next steps

- Build a body: [guides/build-from-source.md](../guides/build-from-source.md)
- Pack zips: [guides/pack-a-release.md](../guides/pack-a-release.md)
- Port notes: [guides/add-or-port-a-body.md](../guides/add-or-port-a-body.md)
