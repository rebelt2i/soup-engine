# Pack a release

Last reviewed: 2026-10

## Local pack

After Classic `SE.BIN` and Film-in-ML builds exist:

```sh
make -C src test && make -C src arm

make -C src/ml/payload PLATFORM=5DC.111
mkdir -p dist/classic-stage
cp card/AUTOEXEC.BIN dist/classic-stage/AUTOEXEC.BIN
cp src/ml/payload/soupeng.bin dist/classic-stage/SE.BIN

python3 src/tools/build-ml.py --platform 50D.109
python3 src/tools/build-ml.py --platform 6D.116
python3 src/tools/build-ml.py --platform 5D3.123

python3 src/tools/pack-release.py --tag v0.2.0-beta \
  --classic-dir dist/classic-stage
```

Optional: `--platforms 50D.109` to limit which Film-in-ML zips are built.

Outputs: `dist/soup-engine-<tag>-<PLATFORM>.zip`.

## CI / GitHub Releases

- Every successful push to `master` / `main` publishes continuous zips via
  `.github/workflows/ci.yml` (`master-<run>-<sha>`).
- Versioned releases: push a `v*` tag or run the **Release** workflow
  (`workflow_dispatch`) — `.github/workflows/release.yml`.

Agent workflow recipe: `.github/skills/pack-release/SKILL.md`.
