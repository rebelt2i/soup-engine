# ADR 002: EOS 50D ships Film-in-ML only (no SE.BIN)

- Status: Accepted
- Date: 2026-10-25

## Context

An earlier 50D approach loaded freestanding `SE.BIN` from the heap and tried a
GUI/key hook (same broad shape as Classic). On-camera work showed repeated
hard failures: malloc starvation when carving RAM for SE, FIO/cache hangs,
unsafe hooks during sensor clean, and hooks that never delivered keys. The
working product boots Magic Lantern with the Film page built in.

Hard-won detail: [`src/ml/platforms/50D.109/PITFALLS.md`](../src/ml/platforms/50D.109/PITFALLS.md).

## Decision

- **Ship** 50D.109 (and by the same DryOS family rules, 6D.116 / 5D3.123 /
  550D.109) via Film-in-ML only: `python3 src/tools/build-ml.py --platform …`.
- **Do not** run `patch-film.py` on these bodies.
- **Do not** revive heap-loaded `SE.BIN` + GUI hook for 50D without new
  on-camera proof that overturns PITFALLS. Treat “just try the hook again” as
  out of scope for routine agent work.
- Keep `src/ml/platforms/50D.109/PITFALLS.md` as the authoritative negative
  record; do not delete it to “clean up” the Classic tree.

## Consequences

- Agents must not propose Classic-style patch/SE packaging for 50D/6D/5D3/550D.
- Memory-layout “fixes” that raise `user_mem_start` / `bss_end` for SE on 50D
  are rejected unless accompanied by new evidence and an ADR update.
- Porting notes live under `integrations/magiclantern/<PLATFORM>/`.
