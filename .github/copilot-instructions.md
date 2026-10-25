# Soup Engine — AI / agent instructions

Film looks for several Canon EOS bodies. Same look engine everywhere; you
ship a **per-camera zip**. Licence: GPL v2 (`LICENSE`, `NOTICE`).

## Dataflow

```text
.fs stocks + CR2  →  src/engine (look)  →  Classic SE.BIN+patch
                                        →  Film-in-ML rebuilt AUTOEXEC
                                        →  dist zip (pack-release.py)
```

Desktop path: same engine via `src/host/` → `filmdev`.

## Key directories

| Path | Role |
|------|------|
| `src/engine/` | Freestanding C99 look engine (host + camera) |
| `src/ml/payload/` | Classic runtime (`film.c`): picker, queue |
| `src/ml/platforms/` | Classic per-body: `cam.h`, `patch.json`, … |
| `integrations/magiclantern/` | Film-in-ML overlays (`_common` + per body) |
| `src/stocks/` | Thirteen film looks (plain text `.fs`) |
| `src/tools/` | `build-ml.py`, `patch-film.py`, `pack-release.py`, … |
| `src/host/` | Desktop `filmdev` |
| `card/` | Install tree template (AUTOEXEC, stocks, …) |
| `docs/` | System / feature / how-to docs |
| `ADRs/` | Settled decisions |
| `.github/workflows/` | `ci.yml` (push/PR), `release.yml` (`v*` tags) |

## Platforms

| Platform | Body | Family | Build |
|----------|------|--------|-------|
| `5DC.111` | 5D Classic 1.1.1 | **Classic** | `make -C src payload PLATFORM=5DC.111` |
| `40D.111` | 40D 1.1.1 | Classic (experimental) | same; see platform README |
| `50D.109` | 50D 1.0.9 | **Film-in-ML** | `python3 src/tools/build-ml.py --platform 50D.109` |
| `6D.116` | 6D Mark I 1.1.6 | Film-in-ML | `… --platform 6D.116` |
| `5D3.123` | 5D Mark III **1.2.3** | Film-in-ML | `… --platform 5D3.123` |

Classic boots patched ML + `SE.BIN`. Film-in-ML boots rebuilt ML with Film
menu — **does not** boot `SE.BIN`. See [ADR 001](../ADRs/001-two-install-families.md),
[ADR 002](../ADRs/002-50d-film-in-ml-only.md).

## Exact commands

```sh
make -C src test          # default CI gate (no CR2)
make -C src arm           # freestanding ARM946E-S smoke
make -C src payload PLATFORM=5DC.111   # Classic SE.BIN + patch-film

python3 src/tools/build-ml.py --platform 50D.109
python3 src/tools/build-ml.py --platform 6D.116
python3 src/tools/build-ml.py --platform 5D3.123

# Pack (after Classic + Film-in-ML artifacts exist):
mkdir -p dist/classic-stage
cp card/AUTOEXEC.BIN dist/classic-stage/
cp src/ml/payload/soupeng.bin dist/classic-stage/SE.BIN
python3 src/tools/pack-release.py --tag v0.2.0-beta --classic-dir dist/classic-stage
```

Toolchain: Python 3, `make`, host `cc`, `arm-none-eabi-gcc`, `git` (Film-in-ML).
Windows: Git `usr\bin` on `PATH`. Optional `ARM_BINPATH`.

## Cross-cutting conventions

- Engine: freestanding C99 on camera paths; **integer-only** per-pixel; no libc on those paths. Same sources for host and camera.
- Do not invent cameras/firmware versions outside the table above.
- Film-in-ML ML pin: `integrations/magiclantern/<PLATFORM>/SOUP-PIN.txt` (currently `ed3e7c0d` / `2025_release_01`).
- Prefer existing code-adjacent comments; do not add docstrings/markdown to files you did not change.
- Scoped rules: `.github/instructions/*.instructions.md` (engine / classic / film-in-ml / tools).

## Prohibitions

- **Never** run `patch-film.py` on `50D.109`, `6D.116`, or `5D3.123`.
- **Never** revive heap-loaded `SE.BIN` / GUI-hook for 50D without new on-camera proof — read `src/ml/platforms/50D.109/PITFALLS.md` first. Do not raise `user_mem_start` / `bss_end` to “make room” for SE.
- If a test fails: **fix the code, not the assertion**, unless requirements explicitly changed.
- Do not create unsolicited `CHANGES.md` / summary markdown files.
- Do not weaken CI gates or skip `make -C src test` / `arm` for agent-authored changes that touch engine or build paths.

## Deeper docs

| Need | Where |
|------|--------|
| Architecture / onboarding | `docs/system/` |
| Classic / Film-in-ML / engine | `docs/features/` |
| Build, release, port a body | `docs/guides/` |
| 50D hard constraints | `src/ml/platforms/50D.109/PITFALLS.md` |
| Per-body Film-in-ML notes | `integrations/magiclantern/<PLATFORM>/NOTES.md` |
| Source layout | `src/README.md` |
| User install | root `README.md` |
