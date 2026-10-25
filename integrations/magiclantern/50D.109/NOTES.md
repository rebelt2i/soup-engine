# 50D.109

Film-in-ML port of the Soup Engine for the EOS 50D, firmware **1.0.9**.

- Boot: classic Digic 4/5 `boot-d45.o`.
- Do not use `patch-film.py` on this body; see `src/ml/platforms/50D.109/PITFALLS.md`.
- Build: `python3 src/tools/build-ml.py --platform 50D.109` (or `build-50d.py`).
