#include "ui_render.h"

#include <string.h>

#include "lcd.h"

static UIGlyph8Provider g_glyph8Provider = NULL;

static bool getFallbackGlyph8(char character, uint8_t outGlyph[8]) {
    const uint8_t *glyphData = NULL;
    static const uint8_t glyphSpace[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
    static const uint8_t glyphDot[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x18, 0x00};
    static const uint8_t glyph0[8] = {0x3C, 0x42, 0x46, 0x4A, 0x52, 0x62, 0x42, 0x3C};
    static const uint8_t glyph1[8] = {0x18, 0x38, 0x18, 0x18, 0x18, 0x18, 0x18, 0x3C};
    static const uint8_t glyph2[8] = {0x3C, 0x42, 0x02, 0x0C, 0x10, 0x20, 0x40, 0x7E};
    static const uint8_t glyph3[8] = {0x3C, 0x42, 0x02, 0x1C, 0x02, 0x02, 0x42, 0x3C};
    static const uint8_t glyph4[8] = {0x08, 0x18, 0x28, 0x48, 0x7E, 0x08, 0x08, 0x08};
    static const uint8_t glyph5[8] = {0x7E, 0x40, 0x40, 0x7C, 0x02, 0x02, 0x42, 0x3C};
    static const uint8_t glyph6[8] = {0x1C, 0x20, 0x40, 0x7C, 0x42, 0x42, 0x42, 0x3C};
    static const uint8_t glyph7[8] = {0x7E, 0x02, 0x04, 0x08, 0x10, 0x10, 0x10, 0x10};
    static const uint8_t glyph8[8] = {0x3C, 0x42, 0x42, 0x3C, 0x42, 0x42, 0x42, 0x3C};
    static const uint8_t glyph9[8] = {0x3C, 0x42, 0x42, 0x42, 0x3E, 0x02, 0x04, 0x38};
    static const uint8_t glyphC[8] = {0x3C, 0x42, 0x40, 0x40, 0x40, 0x40, 0x42, 0x3C};
    static const uint8_t glyphD[8] = {0x78, 0x44, 0x42, 0x42, 0x42, 0x42, 0x44, 0x78};
    static const uint8_t glyphE[8] = {0x7E, 0x40, 0x40, 0x7C, 0x40, 0x40, 0x40, 0x7E};
    static const uint8_t glyphI[8] = {0x7E, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x7E};
    static const uint8_t glyphK[8] = {0x42, 0x44, 0x48, 0x70, 0x48, 0x44, 0x42, 0x41};
    static const uint8_t glyphM[8] = {0x42, 0x66, 0x5A, 0x5A, 0x42, 0x42, 0x42, 0x42};
    static const uint8_t glyphN[8] = {0x42, 0x62, 0x52, 0x4A, 0x46, 0x42, 0x42, 0x42};
    static const uint8_t glyphO[8] = {0x3C, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x3C};
    static const uint8_t glyphR[8] = {0x78, 0x44, 0x44, 0x78, 0x50, 0x48, 0x44, 0x42};
    static const uint8_t glyphS[8] = {0x3C, 0x42, 0x40, 0x30, 0x0C, 0x02, 0x42, 0x3C};
    static const uint8_t glyphT[8] = {0x7E, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18};
    static const uint8_t glyphU[8] = {0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x3C};

    switch (character) {
        case ' ':
            glyphData = glyphSpace;
            break;
        case '.':
            glyphData = glyphDot;
            break;
        case '0':
            glyphData = glyph0;
            break;
        case '1':
            glyphData = glyph1;
            break;
        case '2':
            glyphData = glyph2;
            break;
        case '3':
            glyphData = glyph3;
            break;
        case '4':
            glyphData = glyph4;
            break;
        case '5':
            glyphData = glyph5;
            break;
        case '6':
            glyphData = glyph6;
            break;
        case '7':
            glyphData = glyph7;
            break;
        case '8':
            glyphData = glyph8;
            break;
        case '9':
            glyphData = glyph9;
            break;
        case 'C':
            glyphData = glyphC;
            break;
        case 'D':
            glyphData = glyphD;
            break;
        case 'E':
            glyphData = glyphE;
            break;
        case 'I':
            glyphData = glyphI;
            break;
        case 'K':
            glyphData = glyphK;
            break;
        case 'M':
            glyphData = glyphM;
            break;
        case 'N':
            glyphData = glyphN;
            break;
        case 'O':
            glyphData = glyphO;
            break;
        case 'R':
            glyphData = glyphR;
            break;
        case 'S':
            glyphData = glyphS;
            break;
        case 'T':
            glyphData = glyphT;
            break;
        case 'U':
            glyphData = glyphU;
            break;
        default:
            return false;
    }

    memcpy(outGlyph, glyphData, 8);
    return true;
}

static bool isBitmapPixelOn(const uint16_t *rows, int width, int row, int col) {
    return (rows[row] & (uint16_t)(1U << (width - 1 - col))) != 0U;
}

static void rotatePoint(int width, int height, int col, int row, UIRotation rotation, int *outX, int *outY) {
    switch (rotation) {
        case UI_ROTATE_90_CCW:
            *outX = row;
            *outY = width - 1 - col;
            break;

        case UI_ROTATE_180:
            *outX = width - 1 - col;
            *outY = height - 1 - row;
            break;

        case UI_ROTATE_270_CCW:
            *outX = height - 1 - row;
            *outY = col;
            break;

        case UI_ROTATE_0:
        default:
            *outX = col;
            *outY = row;
            break;
    }
}

void UI_SetPixel(int x, int y, bool on) {
    LCD_BufferSetVisualPixel(x, y, on);
}

void UI_DrawHLine(int x, int y, int width) {
    for (int i = 0; i < width; i++) {
        UI_SetPixel(x + i, y, true);
    }
}

void UI_DrawVLine(int x, int y, int height) {
    for (int i = 0; i < height; i++) {
        UI_SetPixel(x, y + i, true);
    }
}

void UI_DrawRect(int x, int y, int width, int height) {
    if (width <= 0 || height <= 0) {
        return;
    }

    UI_DrawHLine(x, y, width);
    UI_DrawHLine(x, y + height - 1, width);
    UI_DrawVLine(x, y, height);
    UI_DrawVLine(x + width - 1, y, height);
}

void UI_FillRect(int x, int y, int width, int height) {
    for (int row = 0; row < height; row++) {
        UI_DrawHLine(x, y + row, width);
    }
}

void UI_ClearRect(int x, int y, int width, int height) {
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            UI_SetPixel(x + col, y + row, false);
        }
    }
}

static float clampUnit(float value) {
    if (value < 0.0f) {
        return 0.0f;
    }
    if (value > 1.0f) {
        return 1.0f;
    }
    return value;
}

void UI_DrawRangeProfile(int x, int y, int width, int height,
                         const float *samples, int count, float threshold) {
    int bottom;
    int thresholdY;

    if (samples == NULL || count <= 0 || width <= 0 || height <= 0) {
        return;
    }

    UI_ClearRect(x, y, width, height);

    bottom = y + height - 1;
    thresholdY = bottom - (int)(clampUnit(threshold) * (float)(height - 1) + 0.5f);

    for (int drawX = 0; drawX < width; drawX++) {
        int sampleIndex = (drawX * count) / width;
        float sample;
        int barTop;

        if (sampleIndex >= count) {
            sampleIndex = count - 1;
        }

        sample = clampUnit(samples[sampleIndex]);
        barTop = bottom - (int)(sample * (float)(height - 1) + 0.5f);
        UI_DrawVLine(x + drawX, barTop, bottom - barTop + 1);

        if ((drawX & 0x01) == 0) {
            UI_SetPixel(x + drawX, thresholdY, true);
        }
    }
}

void UI_DrawBitmapRows(int x, int y, int width, int height, const uint16_t *rows, UIRotation rotation) {
    if (rows == NULL || width <= 0 || width > 16 || height <= 0) {
        return;
    }

    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            int drawX;
            int drawY;

            if (!isBitmapPixelOn(rows, width, row, col)) {
                continue;
            }

            rotatePoint(width, height, col, row, rotation, &drawX, &drawY);
            UI_SetPixel(x + drawX, y + drawY, true);
        }
    }
}

void UI_DrawGlyph8(int x, int y, const uint8_t glyph[8], UIRotation rotation) {
    uint16_t rows[8];

    if (glyph == NULL) {
        return;
    }

    for (int i = 0; i < 8; i++) {
        rows[i] = (uint16_t)glyph[i];
    }

    UI_DrawBitmapRows(x, y, 8, 8, rows, rotation);
}

void UI_DrawGlyph16(int x, int y, const uint16_t glyph[16], UIRotation rotation) {
    UI_DrawBitmapRows(x, y, 16, 16, glyph, rotation);
}

void UI_SetGlyph8Provider(UIGlyph8Provider provider) {
    g_glyph8Provider = provider;
}

void UI_DrawChar8(int x, int y, char character) {
    uint8_t glyph[8];
    UIGlyph8Provider provider = g_glyph8Provider != NULL ? g_glyph8Provider : getFallbackGlyph8;

    if (provider(character, glyph)) {
        UI_DrawGlyph8(x, y, glyph, UI_ROTATE_0);
    }
}

void UI_DrawText8(int x, int y, const char *text, int spacing) {
    int cursorX = x;

    if (text == NULL) {
        return;
    }

    for (int i = 0; text[i] != '\0'; i++) {
        UI_DrawChar8(cursorX, y, text[i]);
        cursorX += 8 + spacing;
    }
}
