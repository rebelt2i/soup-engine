# Building from source

Photographers: you do not need this page. Download a per-body zip from
[Releases](https://github.com/rebelt2i/soup-engine-50d/releases/latest)
and follow the root [README](../README.md).

This page is for developers who want to rebuild Soup Engine or change it.

## Requirements

- Python 3
- `make`, host `cc` (for desktop tests)
- `arm-none-eabi-gcc` (camera builds)
- `git` (Film-in-ML clones Magic Lantern)
- On Windows: Git’s `usr\bin` on `PATH` so Magic Lantern makefiles find `sh`
- Optional: set `ARM_BINPATH` to the directory that contains `arm-none-eabi-gcc`

## Host tests

```sh
make -C src test    # filmdev selftest + lookcheck
make -C src arm     # freestanding ARM946E-S smoke compile
```

## Classic (5D Classic) — SE.BIN + patch

Needs Magic Lantern’s stock `autoexec.bin` at
`src/vendor/magiclantern-5Dc/autoexec.bin` (not shipped; see
[builds.magiclantern.fm/5DC.html](https://builds.magiclantern.fm/5DC.html)).

```sh
make -C src payload PLATFORM=5DC.111
# runs ml/payload then tools/patch-film.py
```

CI release builds rebuild `SE.BIN` from source and pair it with the
patched `card/AUTOEXEC.BIN` already in this repo. Re-running the binary
patch still needs the vendor stock file locally.

40D is experimental; see `src/ml/platforms/40D.111/README.md`.

## Film-in-ML (50D / 6D / 5D3)

```sh
python3 src/tools/build-ml.py --platform 50D.109
python3 src/tools/build-ml.py --platform 6D.116 --card /path/to/card
python3 src/tools/build-ml.py --platform 5D3.123 --card /path/to/card
```

Clones Magic Lantern at the pin in
`integrations/magiclantern/<PLATFORM>/SOUP-PIN.txt`, overlays
`integrations/magiclantern/`, and builds `AUTOEXEC.BIN` plus the matching
`.sym`. Do **not** run `patch-film.py` on these bodies.

## Packaging a release locally

```sh
# After Classic SE.BIN + Film-in-ML builds exist:
mkdir -p dist/classic-stage
cp card/AUTOEXEC.BIN dist/classic-stage/
cp src/ml/payload/soupeng.bin dist/classic-stage/SE.BIN

python3 src/tools/pack-release.py --tag v0.2.0-beta \
  --classic-dir dist/classic-stage
```

Or push a `v*` tag / run the **Release** workflow on GitHub.

## More detail

See [src/README.md](../src/README.md) for layout, platforms, and licence.
