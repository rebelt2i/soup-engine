---
applyTo: "src/tools/**"
---

# Build tools (`src/tools`)

## Contracts

| Tool | Use for | Do not use for |
|------|---------|----------------|
| `build-ml.py` | Film-in-ML (`50D.109`, `6D.116`, `5D3.123`) | Classic patching |
| `build-50d.py` | Thin wrapper → `50D.109` | Other platforms |
| `patch-film.py` | Classic `5DC.111` / `40D.111` only | Any Film-in-ML body |
| `pack-release.py` | Per-body release zips | Replacing CI host tests |

## Rules

- Keep platform allowlists explicit; reject or no-op unsafe Classic/Film mixes.
- Film-in-ML clone/overlay must respect `integrations/magiclantern/<PLATFORM>/SOUP-PIN.txt`.
- Pack output naming: `dist/soup-engine-<tag>-<PLATFORM>.zip` (see release workflow).
- Prefer exact CLI flags already used in `.github/workflows/ci.yml` and `release.yml`.

## Pointers

- Pack guide: `docs/guides/pack-a-release.md`
- Skill: `.github/skills/pack-release/SKILL.md`
- Source overview: `src/README.md`
