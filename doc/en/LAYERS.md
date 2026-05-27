# LCD UI Layer Notes

## 1. Framebuffer Layer

Files:

- `core/lcd.h`
- `core/lcd.c`

Current responsibilities:

- Owns `g_frameBuffer` as the target frame.
- Converts visual coordinates into the LCD native page/bit layout.
- Stores framebuffer data and drawing results only.

Current coupling:

- No hardware transport coupling.

For open-source release, this layer is the bottom of the package.

## 2. Visual Drawing Layer

Files:

- `core/ui_render.h`
- `core/ui_render.c`

Current responsibilities:

- Draw pixel, line, rectangle, filled rectangle, and clear rectangle.
- Draw bitmap rows.
- Draw 8x8 and 16x16 glyph bitmaps.
- Draw a simple range profile curve.

Current coupling:

- Calls `LCD_BufferSetVisualPixel()`.
- No hardware or CMSIS coupling.

## 3. Text and Glyph Layer

Files:

- `core/ui_font.h`
- `core/ui_font.c`
- `font/ui_font_generated.h`
- `font/ui_font_generated.c`

Current responsibilities:

- Decode UTF-8 text.
- Find glyphs by Unicode codepoint.
- Draw glyphs through the visual drawing layer.
- Measure UTF-8 text width.
- Fall back to `?` when a glyph is missing.

Generated font shape:

```c
typedef struct {
    uint32_t codepoint;
    uint8_t width;
    uint8_t height;
    uint8_t advance;
    int8_t x_offset;
    int8_t y_offset;
    const uint16_t *rows;
} UiGlyph;
```

## 4. Legacy Font Path

Files:

None.

The older ASCII/number drawing path has been removed. The UTF-8 path is the only text API in the package.

## 5. Tool Layer

Files:

- `tools/ui/*`
- `tools/output/*`

Current responsibilities:

- Edit and generate glyph data.
- Export firmware C font files.
- Keep shared character-list and glyph-source output files.
