#!/usr/bin/env python3
"""
Build the EOS 50D Magic Lantern autoexec with the Soup Film menu.

Thin wrapper around build-ml.py --platform 50D.109. Prefer that script
for other DryOS bodies (6D.116, 5D3.123).

    python3 tools/build-50d.py
    python3 tools/build-50d.py --card I:\\

Do not use tools/patch-film.py for the 50D. That plants a GUI hook the
body does not survive. See ml/platforms/50D.109/PITFALLS.md.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [os.path.join(HERE, "build-ml.py"), "--platform", "50D.109"] + sys.argv[1:]
runpy.run_path(os.path.join(HERE, "build-ml.py"), run_name="__main__")
