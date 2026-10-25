# ADR 001: Two install families (Classic vs Film-in-ML)

- Status: Accepted
- Date: 2026-10-25

## Context

Soup Engine ships one look engine to several Canon bodies. Bodies differ in
OS (VxWorks Digic II/III Classic vs DryOS Digic 4/5) and in how Magic Lantern
boots. A single “patch AUTOEXEC + load SE.BIN” story does not fit every camera.

## Decision

Maintain **two install families** that share `src/engine` and `src/stocks`:

| Family | Platforms | Ship artifact | Build |
|--------|-----------|---------------|-------|
| **Classic** | `5DC.111` (released), `40D.111` (experimental) | Patched `AUTOEXEC.BIN` + `SE.BIN` | `make payload` + `patch-film.py` |
| **Film-in-ML** | `50D.109`, `6D.116`, `5D3.123` | Rebuilt ML `AUTOEXEC.BIN` + `.sym` | `tools/build-ml.py` |

Film-in-ML bodies do **not** boot `SE.BIN`. Classic does not use the Film-in-ML
overlay tree under `integrations/magiclantern/`.

## Consequences

- Agents and humans must pick the family before choosing tools (`patch-film` vs `build-ml`).
- Release packaging (`pack-release.py`) produces one zip per platform with the correct card layout.
- New bodies join exactly one family; do not invent a third boot story without a new ADR.
- See also [ADR 002](002-50d-film-in-ml-only.md) for why 50D is Film-in-ML only.
