MODEL = 6D
FW_VERSION = 116

TOP_DIR = ../..

AUTOEXEC_BASE = 0x800000
FIR_BASE = 0x800120

#CANON_FIR = 6D000116.FIR
MAIN_FIRMWARE_ADDR = 0xFF0C0000
PLATFORM_ARCH = armv5te

# Load ML at the beginning of the AllocateMemory pool
# default 0x44C000 - 0xD3C000, patched to 0x4E0000 - 0xD3C000 (592K for us).
RESTARTSTART = 0x44C100
ML_BOOT_OBJ = boot-d45-am.o

ML_BITRATE_OBJ = bitrate-5d3.o
ML_SOUND_CODEC_OBJ = ak4646.o

SOUP_ENGINE := $(TOP_DIR)/../../engine
ML_SRC_EXTRA_OBJS = $(BUILD_DIR)/afma.o $(BUILD_DIR)/reloc.o $(BUILD_DIR)/gps.o \
    $(BUILD_DIR)/film_menu.o $(BUILD_DIR)/film_develop.o \
    $(BUILD_DIR)/soup_se.o $(BUILD_DIR)/soup_cr2.o \
    $(BUILD_DIR)/soup_jpeg_dec.o $(BUILD_DIR)/soup_jpeg_enc.o \
    $(BUILD_DIR)/soup_look.o $(BUILD_DIR)/soup_stock.o \
    $(BUILD_DIR)/soup_wb.o $(BUILD_DIR)/soup_color.o \
    $(BUILD_DIR)/soup_grade.o $(BUILD_DIR)/soup_lut.o

include ../Makefile
.DEFAULT_GOAL := $(BUILD_DIR)/cam_complete

$(BUILD_DIR)/soup_%.o: $(SOUP_ENGINE)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $(CDEPS_FLAGS) -I$(SOUP_ENGINE) -c -o $@ $<

$(BUILD_DIR)/film_develop.o: $(SRC_DIR)/film_develop.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $(CDEPS_FLAGS) -I$(SOUP_ENGINE) -c -o $@ $< $(INCLUDE_ARGS) $(LFLAGS)
