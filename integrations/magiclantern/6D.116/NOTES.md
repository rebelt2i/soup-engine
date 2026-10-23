# 6D.116

Film-in-ML port of the Soup Engine for the EOS 6D Mark I, firmware **1.1.6**.

- Boot: `boot-d45-am.o` (AllocateMemory pool), not the 50D-style BSS resize. Do not copy 50D boot assumptions.
- SD card body; paths still go through Magic Lantern's card APIs.
- Playback JPEG size in `soup_cam.h` is Canon's Small JPEG (2736×1824); verify on-body if playback rejects the file.
- Build: `python3 src/tools/build-ml.py --platform 6D.116`
