#ifndef UI_RENDER_H
#define UI_RENDER_H

#include <stdbool.h>
#include <stdint.h>

typedef enum {
    UI_ROTATE_0 = 0,
    UI_ROTATE_90_CCW,
    UI_ROTATE_180,
    UI_ROTATE_270_CCW
} UIRotation;

typedef bool (*UIGlyph8Provider)(char character, uint8_t outGlyph[8]);

void UI_SetPixel(int x, int y, bool on);
void UI_DrawHLine(int x, int y, int width);
void UI_DrawVLine(int x, int y, int height);
void UI_DrawRect(int x, int y, int width, int height);
void UI_FillRect(int x, int y, int width, int height);
void UI_ClearRect(int x, int y, int width, int height);
void UI_DrawRangeProfile(int x, int y, int width, int height,
                         const float *samples, int count, float threshold);
void UI_DrawBitmapRows(int x, int y, int width, int height, const uint16_t *rows, UIRotation rotation);
void UI_DrawGlyph8(int x, int y, const uint8_t glyph[8], UIRotation rotation);
void UI_DrawGlyph16(int x, int y, const uint16_t glyph[16], UIRotation rotation);
void UI_SetGlyph8Provider(UIGlyph8Provider provider);
void UI_DrawChar8(int x, int y, char character);
void UI_DrawText8(int x, int y, const char *text, int spacing);

#endif // UI_RENDER_H
