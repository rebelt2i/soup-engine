---
name: pack-release
description: Build Classic + Film-in-ML artifacts and pack per-body release zips.
---

1. Run host gates first:

   ```sh
   make -C src test && make -C src arm
   ```

2. Classic `SE.BIN` staging (matches `.github/workflows/release.yml`):

   ```sh
   make -C src/ml/payload PLATFORM=5DC.111
   mkdir -p dist/classic-stage
   cp card/AUTOEXEC.BIN dist/classic-stage/AUTOEXEC.BIN
   cp src/ml/payload/soupeng.bin dist/classic-stage/SE.BIN
   ```

   Do not require a fresh `patch-film.py` for CI-style packing when using the
   repo’s `card/AUTOEXEC.BIN`; local re-patch still needs vendor stock AUTOEXEC.

3. Film-in-ML (set `ARM_BINPATH` if needed):

   ```sh
   python3 src/tools/build-ml.py --platform 50D.109
   python3 src/tools/build-ml.py --platform 6D.116
   python3 src/tools/build-ml.py --platform 5D3.123
   python3 src/tools/build-ml.py --platform 550D.109
   ```

4. Pack:

   ```sh
   python3 src/tools/pack-release.py \
     --tag v0.2.0-beta \
     --classic-dir dist/classic-stage
   ```

   Optional: `--platforms 50D.109` to limit Film-in-ML zips.

5. Versioned GitHub Release: push a `v*` tag or run the **Release** workflow
   (`workflow_dispatch`). Continuous `master-<run>-<sha>` releases come from `ci.yml`.

6. Confirm zips: `dist/soup-engine-<tag>-5DC.111.zip` (and 50D / 6D / 5D3).
   Each zip should include `LICENSE`, `NOTICE`, `INSTALL.txt`.

See `docs/guides/pack-a-release.md`.
