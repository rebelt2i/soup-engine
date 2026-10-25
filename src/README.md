# Source

All of it. The engine, the camera payload, the desktop tools, the
simulator and the film stocks.

## Layout

| | |
|:--|:--|
| `engine/` | the look, the stock format, the CR2 reader, the JPEG codec. Freestanding C99, integer only on every per-pixel path, no libc. The same files build for the camera and for the desktop. |
| `ml/payload/` | Classic freestanding runtime (`film.c`): trash-button picker, watcher, develop queue. |
| `ml/platforms/` | one directory per Classic body (`5DC.111`, `40D.111`, …): `cam.h`, `mlmap.h`, `payload.ld`, `mlstub.S`, `patch.json`. |
| `host/` | `filmdev`, the desktop driver. Develops frames, builds contact sheets, writes cards. |
| `tools/` | Film-in-ML builder, Classic patcher, simulator, cross-checks. |
| `stocks/` | the thirteen films, as plain text. |
| `vendor/` | Magic Lantern checkouts / vendor AUTOEXEC binaries (not shipped). |

Film-in-ML overlays (shared Film page + per-camera Makefile) live outside
`src/`, under [`../integrations/magiclantern/`](../integrations/magiclantern/).

## Platforms

Two install families share one look engine:

| Family | Platforms | How to build |
|:--|:--|:--|
| **Classic** (VxWorks) | `5DC.111`, `40D.111` | `make payload` + `patch-film.py` |
| **Film-in-ML** (DryOS) | `50D.109`, `6D.116`, `5D3.123` | `tools/build-ml.py --platform …` |

```sh
# Classic
make payload PLATFORM=5DC.111
python3 tools/patch-film.py --platform 5DC.111

make payload PLATFORM=40D.111   # needs vendor autoexec + confirmed holes
python3 tools/patch-film.py --platform 40D.111

# Film-in-ML
python3 tools/build-ml.py --platform 50D.109
python3 tools/build-ml.py --platform 6D.116 --card /path/to/card
python3 tools/build-ml.py --platform 5D3.123 --card /path/to/card
```

`PLATFORM` in the top-level Makefile still defaults to `50D.109` for local
sim/host convenience; pass it explicitly for Classic work.

Day-to-day install for each body is in the root [README](../README.md).

## Building

```sh
make all        # the desktop tools
make test       # host selftest + lookcheck (no CR2 needed)
make simtest    # the real payload against a mock camera, byte for byte
make arm        # check the engine still builds freestanding for ARM946E-S
make payload    # SE.BIN for Classic (needs PLATFORM=5DC.111 or 40D.111)
```

`make test` is the default gate: `filmdev selftest` (debayer, stocks,
parsers, look budget, …) and `out/lookcheck` (streaming look vs an
independent whole-image reference, including `soup800.fs`). No sample
raws required. `make simtest` needs a CR2 under `samples/` and a POSIX
host (`pthread`); that is the byte-exact camera/desktop contract.

You need `arm-none-eabi-gcc` for the camera build and nothing unusual
for the rest.

## AUTOEXEC.BIN

### Classic — 5DC.111

Magic Lantern's program for the 5D Classic, with the loader and the
button hook written into padding gaps and the init-task pointer aimed at
`se_boot`. `tools/patch-film.py` applies that using
`ml/platforms/5DC.111/patch.json`, and recomputes the checksum so the
camera still accepts the file. The file stays the same length.

```sh
make payload PLATFORM=5DC.111
python3 tools/patch-film.py --platform 5DC.111
```

`make payload` needs Magic Lantern's `autoexec.bin` under
`vendor/magiclantern-5Dc/`. That binary is theirs to distribute, so it is
not included here.

### Classic — 40D.111 (experimental)

Same contract as the 5D Classic. Digic III / VxWorks. See
[`ml/platforms/40D.111/README.md`](ml/platforms/40D.111/README.md):

- No official builds.magiclantern.fm zip.
- Prove FIO on your experimental AUTOEXEC first.
- Vendor binary: `vendor/magiclantern-40D/autoexec.bin`.
- `patch.json` ships with `holes_confirmed: false` until stub/gui/init
  addresses are rediscovered for that binary.

### Film-in-ML — 50D.109, 6D.116, 5D3.123

These bodies boot a Magic Lantern `autoexec.bin` rebuilt with the Film
page. They do not boot `SE.BIN`. Do not run `patch-film.py` on them.

```sh
python3 tools/build-ml.py --platform 50D.109
python3 tools/build-ml.py --platform 6D.116
python3 tools/build-ml.py --platform 5D3.123
```

The script checks out Magic Lantern `ed3e7c0d`
(`2025_release_01`) under `vendor/magiclantern/`, copies
`integrations/magiclantern/_common/` then the platform overlay, and builds
`platform/<PLATFORM>`. Shared Film sources live in `_common/`; per-camera
playback sizes and Makefiles live under each platform directory.

| Platform | Boot object | Firmware | Sym on card |
|:--|:--|:--|:--|
| `50D.109` | `boot-d45.o` | 1.0.9 | `ML/modules/50D_109.sym` |
| `6D.116` | `boot-d45-am.o` (AllocateMemory) | 1.1.6 | `ML/modules/6D_116.sym` |
| `5D3.123` | `boot-d45.o` | 1.2.3 | `ML/modules/5D3_123.sym` |

You need `arm-none-eabi-gcc` (`ARM_BINPATH`) and, on Windows, Git's
`usr\bin` on `PATH` so the Magic Lantern makefiles can find `sh`.

* Their source: <https://github.com/reticulatedpines/magiclantern_simplified>
* Builds: <https://builds.magiclantern.fm/>

## Licence

GPL v2. See [../LICENSE](../LICENSE).
