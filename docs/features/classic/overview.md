# Feature: Classic (SE.BIN + patch)

Last reviewed: 2026-10

## What it is

On VxWorks Classic bodies, Soup Engine ships as freestanding `SE.BIN`
(`soupeng.bin` from `src/ml/payload/`) plus a same-length patched Magic
Lantern `AUTOEXEC.BIN`. `tools/patch-film.py` applies
`src/ml/platforms/<PLATFORM>/patch.json` (loader / button hook / checksum).

Released: `5DC.111`. Experimental: `40D.111`.

## Why it exists

Classic ML can boot a separate payload from card; the trash-button picker
and develop queue live in the payload, not inside a rebuilt Film menu.

## Invariants

- Family is **Classic only** — see [ADR 001](../../../ADRs/001-two-install-families.md).
- Vendor stock `autoexec.bin` is required to re-run the binary patch; it is
  not shipped (`src/vendor/magiclantern-5Dc/` or `magiclantern-40D/`).
- CI may pair rebuilt `SE.BIN` with the repo’s already-patched
  `card/AUTOEXEC.BIN`.
- Do not use this path for 50D/6D/5D3 ([ADR 002](../../../ADRs/002-50d-film-in-ml-only.md)).

## Build

```sh
make -C src payload PLATFORM=5DC.111
```

## Related

- `src/README.md` (AUTOEXEC section)
- `.github/instructions/classic.instructions.md`
- UI / card layout: root README
