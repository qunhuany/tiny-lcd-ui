#ifndef UI_FONT_H
#define UI_FONT_H

#include <stdint.h>

typedef struct {
    uint32_t codepoint;
    uint8_t width;
    uint8_t height;
    uint8_t advance;
    int8_t x_offset;
    int8_t y_offset;
    const uint16_t *rows;
} UiGlyph;

typedef struct {
    const UiGlyph *glyphs;
    uint16_t count;
    uint8_t line_height;
} UiFont;

const UiGlyph *UI_FindGlyph(const UiFont *font, uint32_t codepoint);
int UI_DrawGlyphEx(int x, int lineTopY, const UiGlyph *glyph);
int UI_DrawUtf8Text(int x, int lineTopY, const UiFont *font, const char *text, int spacing);
int UI_MeasureUtf8Text(const UiFont *font, const char *text, int spacing);

#endif // UI_FONT_H
