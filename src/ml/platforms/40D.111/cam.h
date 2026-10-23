/*
 * cam.h - the EOS 40D firmware 1.1.1, as seen from the Classic payload.
 *
 * Same contract as 5DC.111: freestanding blob, Canon ROM by absolute
 * address, no link against Magic Lantern. Digic III / VxWorks.
 *
 * ROM addresses below come from platform/unmaintained/40D.111/stubs.S in
 * the pinned Magic Lantern tree. ML-image addresses (bmp_printf, etc.) are
 * placeholders until a concrete AUTOEXEC is mapped — see README.md.
 *
 * FIO historically fragile on 40D ML: verify card I/O on your AUTOEXEC
 * before chasing patch holes.
 */
#ifndef SE_CAM_H
#define SE_CAM_H

#include <stdint.h>
#include <stddef.h>

/* ------------------------------------------------------------- ROM: memory */
#define CAM_AllocateMemory       0xFFD5B3E8
#define CAM_FreeMemory           0xFFD5B428
#define CAM_GetMemoryInformation 0xFFD5B4F8
/* memcpy: not in 40D stubs.S; confirm from ROM before relying on cam_memcpy. */
#define CAM_memcpy               0xFFD7D718   /* nearby bzero/memset family; VERIFY */

/* --------------------------------------------------------------- ROM: file */
/* Underscore names in stubs.S are the real entry points. */
#define CAM_FIO_OpenFile         0xFFD1682C
#define CAM_FIO_CreateFile       0xFFD168F8
#define CAM_FIO_RemoveFile       0xFFD169BC
#define CAM_FIO_ReadFile         0xFFD16A80
/* SeekFile is missing from the unmaintained stubs — confirm in ROM. */
#define CAM_FIO_SeekFile         0xFFD16B00   /* PLACEHOLDER — verify before use */
#define CAM_FIO_WriteFile        0xFFD16BF0
#define CAM_FIO_CloseFile        0xFFD16CA8
#define CAM_FIO_GetFileSize      0xFFD16D5C
#define CAM_FIO_FindFirstEx      0xFFD164C4
#define CAM_FIO_FindNextEx       0xFFD16628
#define CAM_FIO_FindClose        0xFFD17100

/* Develop-buffer probe — 40D values unknown; left inert like early 5DC work. */
#define CAM_DEVSTATE_PTR         0x00000000
#define CAM_DEVSTATE_BUF         0x28
#define CAM_DEVBUF_ALIAS         0x00800000
#define CAM_DEVBUF_SIZE          0x0005B000
#define CAM_getDevelopBuffer     0x00000000

static inline int cam_mlstr_ok(uintptr_t p)
{
    /* ML image for 40D typically lives at RESTARTSTART 0xB80000. */
    return p >= 0x00B80000 && p < 0x00C00000;
}

static inline int cam_ram_ptr_ok(uintptr_t p)
{
    return p >= 0x00001000 && p < 0x10000000 && (p & 3) == 0;
}

/* ----------------------------------------------------------- ROM: display */
#define CAM_PALETTE_BASE    0xC0F14080
#define CAM_PALETTE_LATCH   0xC0F14078
#define CAM_NotifyBmpOn     0x00000000   /* unused; Classic opens menu via GUI_Control */

#define CAM_GUI_Control     0xFF85BD68
#define SE_BGMT_MENU        0x05
#define SE_FAKE_BTN         (-123456)

/* Button codes from platform/unmaintained/40D.111/gui.h */
#define SE_BTN_WHEEL_UP     0x00
#define SE_BTN_WHEEL_DOWN   0x01
/* No horizontal wheel on this body; sentinels for film.c switch cases. */
#define SE_BTN_WHEEL_LEFT   0x7E
#define SE_BTN_WHEEL_RIGHT  0x7F
#define SE_BTN_SET          0x04
#define SE_BTN_MENU         0x05
#define SE_BTN_INFO         0x06
#define SE_BTN_JUMP         0x07
#define SE_BTN_PLAY         0x08
#define SE_BTN_TRASH        0x09
#define SE_BTN_UNPRESS_UDLR 0x15
#define SE_BTN_UP           0x16
#define SE_BTN_UP_RIGHT     0x17
#define SE_BTN_UP_LEFT      0x18
#define SE_BTN_RIGHT        0x19
#define SE_BTN_LEFT         0x1a
#define SE_BTN_DOWN_RIGHT   0x1b
#define SE_BTN_DOWN_LEFT    0x1c
#define SE_BTN_DOWN         0x1d

#define CAM_ShowBitmap      0x00000000
#define CAM_HideBitmap      0x00000000
#define CAM_bmp_shown       0x00000000

/* TurnOnDisplay: not stubbed for 40D; Classic path uses GUI_Control(MENU). */
#define CAM_TurnOnDisplay   0x00000000
#define CAM_BmpDDev_take    0xFFCB9028
#define CAM_BmpDDev_give    0xFFCB9078

#define CAM_msleep              0xFFD44300
#define CAM_task_create         0xFFD4464C
/* tickGet not in 40D stubs — placeholder; logging timestamps need a real one. */
#define CAM_tickGet             0xFFD44300   /* PLACEHOLDER: currently msleep; replace */

/*
 * Digic II/III Classic: palette is written through PB shadow RAM, not the
 * Digic-4 LCD_Palette + EngDrvOut path. Zero registers so film.c skips EngDrvOut.
 */
#define CAM_EngDrvOut           0x00000000

/* ML-image helpers — valid only for a known AUTOEXEC; fill after mapping. */
#define ML_bmp_printf           0x00B81000   /* PLACEHOLDER */
#define ML_menu_draw_icon       0x00B82000   /* PLACEHOLDER */

#define SE_FONT_PLAIN   0x00030201

#define MEM(x) (*(volatile uint32_t *)(uintptr_t)(x))

typedef int (*se_fn)(void);

#define CAM_CALL0(addr, t)                 (((t (*)(void))(addr))())
#define CAM_CALL1(addr, t, a)              (((t (*)(long))(addr))((long)(a)))
#define CAM_CALL2(addr, t, a, b)           (((t (*)(long,long))(addr))((long)(a),(long)(b)))
#define CAM_CALL3(addr, t, a, b, c)        (((t (*)(long,long,long))(addr))((long)(a),(long)(b),(long)(c)))
#define CAM_CALL4(addr, t, a, b, c, d)     (((t (*)(long,long,long,long))(addr))((long)(a),(long)(b),(long)(c),(long)(d)))
#define CAM_CALL5(addr, t, a, b, c, d, e)  (((t (*)(long,long,long,long,long))(addr))((long)(a),(long)(b),(long)(c),(long)(d),(long)(e)))

static inline void *cam_alloc(size_t n)  { return CAM_CALL1(CAM_AllocateMemory, void *, n); }
static inline void  cam_free(void *p)    { CAM_CALL1(CAM_FreeMemory, void, p); }

static inline void cam_meminfo(int *total, int *freebytes)
{
    CAM_CALL2(CAM_GetMemoryInformation, void, total, freebytes);
}

#define SE_O_RDONLY 0

static inline int cam_open(const char *path)
{
    return CAM_CALL2(CAM_FIO_OpenFile, int, path, SE_O_RDONLY);
}
static inline int cam_create(const char *path)
{
    return CAM_CALL1(CAM_FIO_CreateFile, int, path);
}
static inline int  cam_read (int h, void *buf, size_t n) { return CAM_CALL3(CAM_FIO_ReadFile,  int, h, buf, n); }
static inline int  cam_write(int h, const void *b, size_t n) { return CAM_CALL3(CAM_FIO_WriteFile, int, h, b, n); }
static inline void cam_close(int h) { CAM_CALL1(CAM_FIO_CloseFile, void, h); }
static inline void cam_remove(const char *p) { CAM_CALL1(CAM_FIO_RemoveFile, void, p); }
static inline int  cam_seek (int h, int pos, int whence) { return CAM_CALL3(CAM_FIO_SeekFile, int, h, pos, whence); }

static inline void cam_msleep(int ms) { CAM_CALL1(CAM_msleep, void, ms); }

/* VxWorks / Digic 2–3 uncached alias (same as 5DC). */
#define CAM_UNCACHED_BIT  0x10000000u
#define CAM_UNCACHED(p)   ((void *)((uintptr_t)(p) | CAM_UNCACHED_BIT))
#define CAM_CACHED(p)     ((void *)((uintptr_t)(p) & ~(uintptr_t)CAM_UNCACHED_BIT))

static inline void cam_copy_uncached(void *dst, const void *src, int n)
{
    volatile const uint8_t *u = (volatile const uint8_t *)CAM_UNCACHED(src);
    uint8_t *d = (uint8_t *)dst;
    int i = 0;

    if (((((uintptr_t)d) | ((uintptr_t)u)) & 3) == 0) {
        volatile const uint32_t *uw = (volatile const uint32_t *)(const void *)u;
        uint32_t *dw = (uint32_t *)dst;
        int w = n >> 2;
        for (; i < w; i++) dw[i] = uw[i];
        i <<= 2;
    }
    for (; i < n; i++) d[i] = u[i];
}

static inline int cam_imgbuf_ptr_ok(uintptr_t p)
{
    uintptr_t a = p & ~(uintptr_t)CAM_UNCACHED_BIT;
    return a >= 0x00001000 && a < 0x10000000 && (p & 3) == 0;
}

static inline void cam_memcpy(volatile void *dst, const void *src, size_t n)
{
    CAM_CALL3(CAM_memcpy, void *, dst, src, n);
}

#include "mlmap.h"

static inline uintptr_t cam_overlay_ptr(void)
{
    return (uintptr_t)MEM(CAM_bmp_vram_real_ptr);
}

typedef void (*cam_printf_fn)(uint32_t fontspec, int x, int y, const char *fmt, ...);
#define cam_printf (*(cam_printf_fn)ML_bmp_printf)

static inline void cam_menu_icon(int x, int y, int type, int arg)
{
    CAM_CALL4(ML_menu_draw_icon, void, x, y, type, arg);
}

static inline int cam_test_and_set(volatile int *lock)
{
    int v = 1;
#ifdef __arm__
    __asm__ __volatile__("swp %0, %0, [%1]" : "+r"(v) : "r"(lock) : "memory");
#else
    (void)lock;
#endif
    return v;
}

static inline void cam_release(volatile int *lock)
{
    __asm__ __volatile__("" ::: "memory");
    *lock = 0;
}

static inline uint32_t cam_cpsr(void)
{
#ifdef __arm__
    uint32_t r;
    __asm__ __volatile__("mrs %0, cpsr" : "=r"(r));
    return r;
#else
    return 0;
#endif
}

static inline int cam_panel_ptr_ok(uintptr_t p)
{
    uintptr_t a = (uintptr_t)CAM_CACHED(p);
    if (!a || (a & 3)) return 0;
    if (a >= 0x02000000) return 0;
    if (a >= 0x00B80000 && a < 0x00C00000) return 0;   /* ML's and ours */
    return 1;
}

#endif /* SE_CAM_H */
