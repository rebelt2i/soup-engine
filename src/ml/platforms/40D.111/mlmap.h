/*
 * mlmap.h - display map for the EOS 40D Classic payload.
 *
 * Geometry matches the 5D Classic (720×240, 4-bit, 360-byte pitch).
 * RAM addresses from unmaintained/40D.111 consts and stubs; ML-image
 * addresses are placeholders until a concrete AUTOEXEC is mapped.
 */
#ifndef SE_MLMAP_H
#define SE_MLMAP_H

/*
 * bmp_vram_info stub is 0x1E450. On Digic II/III the real panel pointer is
 * often a nearby shadow value — confirm against your dump. DISPLAY_IS_ON
 * from consts.h.
 */
#define CAM_bmp_vram_real_ptr   0x0001E450   /* bmp_vram_info — VERIFY deref */
#define CAM_display_is_on       0x0000BE9C   /* DISPLAY_IS_ON */

#define ML_menus_display        0x00B85A8C   /* PLACEHOLDER — ML image */

#define CAM_ml_shutdown         0x00BC84E0   /* PLACEHOLDER — ML image */

#define CAM_gui_bmp_ready       0x0000BE9C   /* provisional: same as display_is_on */
#define ML_BMP_PITCH            360
#define ML_BMP_ROWS             240
#define ML_BMP_BYTES            (ML_BMP_PITCH * ML_BMP_ROWS)

/* PB_Palette from stubs.S; 12-byte shadows like Digic II until proven otherwise. */
#define CAM_PB_PALETTE          0x0001E388
#define CAM_PB_PAL_VAL(k)       (CAM_PB_PALETTE + (k) * 12 + 8)
#define CAM_PB_PALETTE_DIRTY    CAM_PB_PAL_VAL(15)
#define CAM_PB_PAL_MINE         CAM_PB_PAL_VAL(6)
#define SE_PAL_MINE_INDEX       6
#define SE_PALETTE_MARK         0x03EB0000

/* Digic-4 EngDrvOut path unused on this body (see cam.h). */
#define CAM_LCD_PALETTE         0
#define CAM_LCD_PAL_REG(k)      0
#define CAM_LCD_PAL_REG2(k)     0

#define ML_palette              0x00BA2BD0   /* PLACEHOLDER — ML image */
#define ML_PALETTE_N            16

#endif /* SE_MLMAP_H */
