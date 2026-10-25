# 40D.111 — Classic path (experimental)

The EOS 40D is Digic III / **VxWorks**, same install family as the 5D Classic:
binary-patch a Magic Lantern `AUTOEXEC.BIN`, boot freestanding `SE.BIN`.
It is **not** a Film-in-ML / DryOS body.

## Status

| Layer | State |
|-------|--------|
| ROM stubs in `cam.h` | Filled from `platform/unmaintained/40D.111/stubs.S` (FW 1.1.1) |
| Button codes | From `gui.h` |
| Display / ML image map | Partial — BMP / palette / ML-internal addresses need a concrete AUTOEXEC |
| `patch.json` holes | **Not confirmed** — stub hole, GUI BL, init literal must be found per binary |
| Official ML builds | **None** on builds.magiclantern.fm |

## Before anything else: FIO

Classic Soup **must** load `A:/SE.BIN` through Canon FIO. 40D Magic Lantern
has historically had broken filesystem support. On the AUTOEXEC you intend to
patch:

1. Boot ML.
2. Confirm the card can be read and written (e.g. ML config, a test file).
3. Only then chase stub holes and payload carve.

Without working FIO, `SE.BIN` never loads and the Classic path cannot ship.

## Vendor binary

Place a bootable 40D.111 `autoexec.bin` at:

```
src/vendor/magiclantern-40D/autoexec.bin
```

Sources for that file are experimental (in-tree `unmaintained/40D.111`, or a
community VxWorks build). There is no official Soup-supported zip.

## Build (once holes are filled)

```sh
make payload PLATFORM=40D.111
python3 tools/patch-film.py --platform 40D.111
```

`patch-film.py` refuses to splice until `patch.json` matches the vendor
binary (same checks as 5DC.111). Placeholder addresses in the current
`patch.json` will fail those checks on purpose.

## Memory sketch

ML restarts at `0x00B80000` and carves heap down from `0x00C00000`
(`Makefile.platform.default`). Payload base in `payload.ld` is a first guess
at `0x00BD0000` (above a typical ML image/bss). Re-measure against your
AUTOEXEC before trusting it.
