# 5D3.123

Film-in-ML port of the Soup Engine for the EOS 5D Mark III, firmware **1.2.3**.

- Boot: classic Digic 4/5 `boot-d45.o` (same family as the 50D).
- Dual card slots: CR2 paths use Magic Lantern's `get_dcim_dir` / shooting card APIs.
- Playback JPEG size in `soup_cam.h` is Canon's Small JPEG (2784×1856); verify on-body if playback rejects the file.
- Build: `python3 src/tools/build-ml.py --platform 5D3.123`
