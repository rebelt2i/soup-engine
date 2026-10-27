# Platforms

Last reviewed: 2026-10

| Platform | Body | Firmware | Family | UI after install | Build |
|----------|------|----------|--------|------------------|-------|
| `5DC.111` | EOS 5D Classic | 1.1.1 | Classic | Trash-button picker | `make -C src payload PLATFORM=5DC.111` |
| `40D.111` | EOS 40D | 1.1.1 | Classic (experimental) | Trash picker | same; see `src/ml/platforms/40D.111/README.md` |
| `50D.109` | EOS 50D | 1.0.9 | Film-in-ML | ML **Film** page | `python3 src/tools/build-ml.py --platform 50D.109` |
| `6D.116` | EOS 6D Mark I | 1.1.6 | Film-in-ML | ML **Film** page | `… --platform 6D.116` |
| `5D3.123` | EOS 5D Mark III | **1.2.3 only** | Film-in-ML | ML **Film** page | `… --platform 5D3.123` |
| `550D.109` | EOS 550D | 1.0.9 | Film-in-ML | ML **Film** page | `… --platform 550D.109` |

## Film-in-ML boot / sym

| Platform | Boot object | Sym on card |
|----------|-------------|-------------|
| `50D.109` | `boot-d45.o` | `ML/modules/50D_109.sym` |
| `6D.116` | `boot-d45-am.o` | `ML/modules/6D_116.sym` |
| `5D3.123` | `boot-d45.o` | `ML/modules/5D3_123.sym` |
| `550D.109` | `boot-d45-am.o` | `ML/modules/550D_109.sym` |

ML pin: `integrations/magiclantern/<PLATFORM>/SOUP-PIN.txt`.

## Hard rules

- Do **not** run `patch-film.py` on Film-in-ML platforms.
- 50D does not ship `SE.BIN` — [ADR 002](../../ADRs/002-50d-film-in-ml-only.md),
  [`PITFALLS.md`](../../src/ml/platforms/50D.109/PITFALLS.md).
- Per-body Film notes: `integrations/magiclantern/<PLATFORM>/NOTES.md`.

User install matrix: root [README.md](../../README.md).
