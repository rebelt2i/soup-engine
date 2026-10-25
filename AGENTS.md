# Agent entry (Soup Engine)

Read **[`.github/copilot-instructions.md`](.github/copilot-instructions.md)**
before editing. That file is the always-on system prompt.

## Must follow

1. Two install families: **Classic** (`5DC.111` / experimental `40D.111`) vs
   **Film-in-ML** (`50D.109`, `6D.116`, `5D3.123`). See `ADRs/`.
2. Never `patch-film.py` on Film-in-ML bodies. Never revive 50D `SE.BIN`
   heap/hook without reading `src/ml/platforms/50D.109/PITFALLS.md`.
3. Default verify: `make -C src test` and `make -C src arm`. Fix code on
   failure, not the assertion.
4. Path-scoped rules: `.github/instructions/`. Workflows: `.github/skills/`.
5. Depth: `docs/system/`, `docs/features/`, `docs/guides/`. Do not invent
   platforms or unsolicited markdown summaries.

User-facing install stays in root `README.md`. Developers: `docs/guides/build-from-source.md`.
