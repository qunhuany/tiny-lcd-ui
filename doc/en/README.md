# Tiny LCD UI User Guide

## What This Project Provides

Tiny LCD UI provides the middle layer of a monochrome LCD UI stack:

- A page-oriented framebuffer.
- Visual-coordinate pixel writing.
- Drawing primitives such as lines, rectangles, bitmaps, and range profiles.
- UTF-8 text drawing with generated bitmap glyphs.
- A Python font editor and firmware font export workflow.

It does not talk to LCD hardware. Your firmware is responsible for uploading
`g_frameBuffer` to the target screen.

Related English documents:

- [Layer notes](LAYERS.md)
- [Open-source preparation notes](OPEN_SOURCE_NOTES.md)

## Layer Model

```text
Application screen code
        |
        v
UTF-8 text layer
        |
        v
Visual drawing layer
        |
        v
Framebuffer layer
        |
        v
Downstream display driver
```

The downstream display driver is not part of this project.

## Core Files

```text
core/lcd.h                 framebuffer dimensions and buffer API
core/lcd.c                 framebuffer storage and visual/native pixel mapping
core/ui_render.h           drawing API
core/ui_render.c           drawing implementation
core/ui_font.h             UTF-8 font API
core/ui_font.c             UTF-8 decoding, glyph lookup, measurement, drawing
font/ui_font_generated.h   generated font declarations
font/ui_font_generated.c   generated glyph data
```

## Framebuffer Layout

The default screen is 128x64.

```c
#define LCD_BUFFER_X_BLOCKS 16
#define LCD_BUFFER_PAGES 8
#define LCD_BUFFER_BLOCK_SIZE 8
```

The framebuffer is:

```c
uint8_t g_frameBuffer[LCD_BUFFER_X_BLOCKS][LCD_BUFFER_PAGES][LCD_BUFFER_BLOCK_SIZE];
```

The visual drawing API uses a top-left origin:

```text
(0, 0) ----------------> x
  |
  |
  v
  y
```

The framebuffer still stores pixels in a page-oriented LCD memory layout, so a
downstream driver can translate it to its own LCD protocol.

## Minimal Rendering Example

```c
#include "lcd.h"
#include "ui_render.h"
#include "ui_font.h"
#include "ui_font_generated.h"

void renderStatusPage(void) {
    LCD_BufferInit();

    UI_DrawRect(0, 0, LCD_VISUAL_WIDTH, LCD_VISUAL_HEIGHT);
    UI_DrawHLine(0, 16, LCD_VISUAL_WIDTH);

    UI_DrawUtf8Text(4, 4, &uiFontDefault, "Tiny LCD UI", 0);
    UI_DrawUtf8Text(4, 24, &uiFontDefault, "Distance: 1.234m", 0);
}
```

After rendering, upload `g_frameBuffer` in your board-specific code.

## Example Upload Boundary

This project does not implement the function below. It shows where your own
driver should begin.

```c
void uploadFrameBufferToDisplay(void) {
    for (int page = 0; page < LCD_BUFFER_PAGES; page++) {
        for (int block = 0; block < LCD_BUFFER_X_BLOCKS; block++) {
            const uint8_t *bytes = g_frameBuffer[block][page];

            /*
             * Your code:
             * - set LCD page/column
             * - write LCD_BUFFER_BLOCK_SIZE bytes
             */
        }
    }
}
```

## Font Workflow

Run the font editor:

```powershell
python tools\ui\font_tool_main.py
```

Typical workflow:

1. Load or edit glyph data.
2. Add required UI characters.
3. Generate missing glyphs from `tools/ui/unifont.ttf`.
4. Export firmware font files.
5. Rebuild firmware with the generated `font/ui_font_generated.*`.

## What To Keep Out

Do not add these to the core package:

- I2C/SPI communication.
- LCD controller initialization commands.
- RTOS mutexes.
- Product menu state machines.
- Radar, measurement, or current-output logic.
- Board schematics or firmware binaries.
