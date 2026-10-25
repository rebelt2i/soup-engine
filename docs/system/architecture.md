# Architecture

Last reviewed: 2026-10

## One-line flow

```text
Film stock (.fs) + CR2  →  look engine (src/engine)
                        →  Classic: SE.BIN + patched AUTOEXEC
                        →  Film-in-ML: rebuilt ML AUTOEXEC + Film menu
                        →  per-body zip (pack-release.py)
```

Desktop develops the same way through `src/host/` (`filmdev`).

## Pieces

| Piece | Responsibility |
|-------|----------------|
| Look engine | Parse stocks, read CR2, grade, JPEG — freestanding C99 |
| Classic runtime | `src/ml/payload/` — trash picker, watcher, develop queue |
| Classic platforms | `src/ml/platforms/<PLATFORM>/` — stubs, linker, `patch.json` |
| Film-in-ML | `integrations/magiclantern/` — Film page inside ML |
| Stocks | `src/stocks/` → card `ML/FILM/*.fs` |
| Tools | Build ML, patch Classic AUTOEXEC, pack zips |
| Card / dist | Install tree template and release staging |

## Install families

See [ADR 001](../../ADRs/001-two-install-families.md). Classic boots patched
Magic Lantern then `SE.BIN`. Film-in-ML boots only the rebuilt AUTOEXEC (Film
menu develops to `FLM_nnnn.JPG` on DryOS bodies; Classic trash-picker path
produces `*.FLM.JPG` beside the CR2 on 5D Classic — see root README).

## Release shape

Each zip is named `soup-engine-<tag>-<PLATFORM>.zip` and includes
`LICENSE`, `NOTICE`, `INSTALL.txt`, the right AUTOEXEC (and `SE.BIN` or
`.sym`), and film stocks. CI: `.github/workflows/ci.yml` (continuous) and
`release.yml` (`v*` / dispatch).

## Related

- [platforms.md](platforms.md)
- [onboarding.md](onboarding.md)
- Feature overviews under `docs/features/`
