# Tiny LCD UI

Tiny LCD UI is a small monochrome LCD UI toolkit for embedded firmware.

The project intentionally stops at the middle layer:

- framebuffer storage
- visual-coordinate drawing
- UTF-8 bitmap text rendering
- bitmap font editing and generation tools

It does not include any screen communication protocol. I2C, SPI, DMA, LCD
controller commands, RTOS locks, and board-specific refresh code should live in
the downstream firmware project.

## Documentation

- English guide: [doc/en/README.md](doc/en/README.md)
- Chinese guide: [doc/cn/README.md](doc/cn/README_cn.md)
- English layer notes: [doc/en/LAYERS.md](doc/en/LAYERS.md)
- Chinese layer notes: [doc/cn/LAYERS.md](doc/cn/LAYERS.md)

## Directory Layout

```text
lcd/
  core/
    lcd.h / lcd.c              framebuffer storage and pixel mapping
    ui_render.h / ui_render.c  visual drawing primitives
    ui_font.h / ui_font.c      UTF-8 glyph lookup, measurement, and drawing

  font/
    ui_font_generated.h/.c     generated firmware bitmap font

  tools/
    ui/                        font editor, glyph backend, source font
    output/                    shared glyph source and collected character lists

  doc/
    en/README.md               English user guide
    cn/README.md               Chinese user guide
```

## Minimal Example

```c
#include "lcd.h"
#include "ui_render.h"
#include "ui_font.h"
#include "ui_font_generated.h"

void renderScreen(void) {
    LCD_BufferClear();

    UI_DrawRect(0, 0, LCD_VISUAL_WIDTH, LCD_VISUAL_HEIGHT);
    UI_DrawUtf8Text(4, 6, &uiFontDefault, "Hello LCD", 0);
    UI_DrawUtf8Text(4, 24, &uiFontDefault, "中文菜单", 0);

    /*
     * Upload g_frameBuffer to your LCD controller in downstream code.
     * This project does not know whether your screen uses I2C, SPI, DMA,
     * ST7565, SSD1306, SH1106, or a custom protocol.
     */
}
```

## Font Tool

The font editor lives under `tools/ui`.

```powershell
python tools\ui\font_tool_main.py
```

The tool keeps edited glyph data under `tools/ui/output` and can export firmware
font files into `font/ui_font_generated.c` and `font/ui_font_generated.h`.

## Scope

This project is meant to be reusable UI middleware. Keep product menus,
measurement algorithms, LCD bus protocol code, and board support packages out of
this repository.

## License

Choose and add a final project license before publishing. Also verify the license
for `tools/ui/unifont.ttf` and the generated glyph data.
