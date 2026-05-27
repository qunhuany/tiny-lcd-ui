#include "ui_font.h"

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "ui_render.h"

static bool decodeUtf8Next(const char **text, uint32_t *codepoint) {
    const uint8_t *s;

    if (text == NULL || *text == NULL || **text == '\0' || codepoint == NULL) {
        return false;
    }

    s = (const uint8_t *)(*text);
    if (s[0] < 0x80U) {
        *codepoint = s[0];
        *text += 1;
        return true;
    }

    if ((s[0] & 0xE0U) == 0xC0U && (s[1] & 0xC0U) == 0x80U) {
        *codepoint = ((uint32_t)(s[0] & 0x1FU) << 6) |
                     (uint32_t)(s[1] & 0x3FU);
        *text += 2;
        return true;
    }

    if ((s[0] & 0xF0U) == 0xE0U && (s[1] & 0xC0U) == 0x80U && (s[2] & 0xC0U) == 0x80U) {
        *codepoint = ((uint32_t)(s[0] & 0x0FU) << 12) |
                     ((uint32_t)(s[1] & 0x3FU) << 6) |
                     (uint32_t)(s[2] & 0x3FU);
        *text += 3;
        return true;
    }

    if ((s[0] & 0xF8U) == 0xF0U && (s[1] & 0xC0U) == 0x80U &&
        (s[2] & 0xC0U) == 0x80U && (s[3] & 0xC0U) == 0x80U) {
        *codepoint = ((uint32_t)(s[0] & 0x07U) << 18) |
                     ((uint32_t)(s[1] & 0x3FU) << 12) |
                     ((uint32_t)(s[2] & 0x3FU) << 6) |
                     (uint32_t)(s[3] & 0x3FU);
        *text += 4;
        return true;
    }

    *codepoint = '?';
    *text += 1;
    return true;
}

const UiGlyph *UI_FindGlyph(const UiFont *font, uint32_t codepoint) {
    int left;
    int right;

    if (font == NULL || font->glyphs == NULL || font->count == 0U) {
        return NULL;
    }

    left = 0;
    right = (int)font->count - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        uint32_t midCodepoint = font->glyphs[mid].codepoint;

        if (midCodepoint == codepoint) {
            return &font->glyphs[mid];
        }
        if (midCodepoint < codepoint) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return NULL;
}

int UI_DrawGlyphEx(int x, int lineTopY, const UiGlyph *glyph) {
    if (glyph == NULL || glyph->rows == NULL) {
        return 0;
    }

    UI_DrawBitmapRows(x + glyph->x_offset, lineTopY + glyph->y_offset,
                      glyph->width, glyph->height, glyph->rows, UI_ROTATE_0);
    return glyph->advance;
}

int UI_DrawUtf8Text(int x, int lineTopY, const UiFont *font, const char *text, int spacing) {
    int cursorX = x;
    bool hasPreviousGlyph = false;

    if (font == NULL || text == NULL) {
        return 0;
    }

    while (*text != '\0') {
        uint32_t codepoint;
        const UiGlyph *glyph;

        if (!decodeUtf8Next(&text, &codepoint)) {
            break;
        }

        if (hasPreviousGlyph) {
            cursorX += spacing;
        }
        hasPreviousGlyph = true;

        if (codepoint == ' ') {
            cursorX += 4;
            continue;
        }

        glyph = UI_FindGlyph(font, codepoint);
        if (glyph == NULL) {
            glyph = UI_FindGlyph(font, '?');
        }

        if (glyph != NULL) {
            cursorX += UI_DrawGlyphEx(cursorX, lineTopY, glyph);
        } else {
            cursorX += 8;
        }
    }

    return cursorX - x;
}

int UI_MeasureUtf8Text(const UiFont *font, const char *text, int spacing) {
    int width = 0;
    bool hasPreviousGlyph = false;

    if (font == NULL || text == NULL) {
        return 0;
    }

    while (*text != '\0') {
        uint32_t codepoint;
        const UiGlyph *glyph;

        if (!decodeUtf8Next(&text, &codepoint)) {
            break;
        }

        if (hasPreviousGlyph) {
            width += spacing;
        }
        hasPreviousGlyph = true;

        if (codepoint == ' ') {
            width += 4;
            continue;
        }

        glyph = UI_FindGlyph(font, codepoint);
        if (glyph == NULL) {
            glyph = UI_FindGlyph(font, '?');
        }
        width += glyph != NULL ? glyph->advance : 8;
    }

    return width;
}
