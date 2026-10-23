/*
 * First-guess payload carve for 40D Magic Lantern at RESTARTSTART 0xB80000
 * with heap base patched down from 0xC00000. Re-measure bss end against
 * your AUTOEXEC before trusting these numbers.
 *
 * 0x00BD0000..0x00C00000 ≈ 192 KB, same split as 5DC (128K image + stacks).
 */
MEMORY
{
    payload (rwx) : ORIGIN = 0x00BD0000, LENGTH = 128K
    mstack  (rw)  : ORIGIN = 0x00BF0000, LENGTH = 16K
    wstack  (rw)  : ORIGIN = 0x00BF4000, LENGTH = 48K
}

ENTRY(_se_header)

SECTIONS
{
    .text : {
        KEEP(*(.header))
        *(.text*)
        *(.rodata*)
        . = ALIGN(4);
    } > payload

    .data : {
        *(.data*)
        . = ALIGN(4);
    } > payload

    .bss (NOLOAD) : {
        __bss_start = .;
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        __bss_end = .;
    } > payload

    __payload_end = .;
    __mstack_top    = ORIGIN(mstack) + LENGTH(mstack);
    __wstack_top    = ORIGIN(wstack) + LENGTH(wstack);
    __wstack_bottom = ORIGIN(wstack);

    /DISCARD/ : { *(.comment) *(.ARM.attributes) *(.note*) }
}
