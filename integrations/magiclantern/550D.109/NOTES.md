# 550D.109

Film-in-ML port of the Soup Engine for the EOS 550D (Rebel T2i), firmware **1.0.9**.

- Boot: `boot-d45-am.o` (AllocateMemory pool). The malloc pool on this body is
  small; do not copy 50D BSS-resize boot assumptions.
- SD card body; paths go through Magic Lantern's card APIs.
- Playback JPEG size in `soup_cam.h` is Canon's Small JPEG (2592×1728); verify
  on-body if playback rejects the file.
- Do not use `patch-film.py` on this body.
- Build: `python3 src/tools/build-ml.py --platform 550D.109`
