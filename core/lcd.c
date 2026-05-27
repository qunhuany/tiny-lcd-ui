#include "lcd.h"

#include <string.h>

uint8_t g_frameBuffer[LCD_BUFFER_X_BLOCKS][LCD_BUFFER_PAGES][LCD_BUFFER_BLOCK_SIZE];

void LCD_BufferInit(void) {
    memset(g_frameBuffer, 0, sizeof(g_frameBuffer));
}

void LCD_BufferClear(void) {
    memset(g_frameBuffer, 0, sizeof(g_frameBuffer));
}

void LCD_BufferSetNativePixel(int rawX, int page, int bit, bool on) {
    uint8_t mask;

    if (rawX < 0 || rawX >= LCD_VISUAL_WIDTH || page < 0 || page >= LCD_BUFFER_PAGES ||
        bit < 0 || bit >= LCD_BUFFER_BLOCK_SIZE) {
        return;
    }

    mask = (uint8_t)(1U << bit);
    if (on) {
        g_frameBuffer[rawX / LCD_BUFFER_BLOCK_SIZE][page][rawX % LCD_BUFFER_BLOCK_SIZE] |= mask;
    } else {
        g_frameBuffer[rawX / LCD_BUFFER_BLOCK_SIZE][page][rawX % LCD_BUFFER_BLOCK_SIZE] &= (uint8_t)(~mask);
    }
}

void LCD_BufferSetVisualPixel(int x, int y, bool on) {
    int rawX;
    int nativeY;

    if (x < 0 || x >= LCD_VISUAL_WIDTH || y < 0 || y >= LCD_VISUAL_HEIGHT) {
        return;
    }

    rawX = (LCD_VISUAL_WIDTH - 1) - x;
    nativeY = (LCD_VISUAL_HEIGHT - 1) - y;
    LCD_BufferSetNativePixel(rawX, nativeY / LCD_BUFFER_BLOCK_SIZE, nativeY % LCD_BUFFER_BLOCK_SIZE, on);
}

void LCD_BufferClearPageRect(int x, int page, int width, int pages) {
    int x_end = x + width;
    int page_end = page + pages;

    if (width <= 0 || pages <= 0) {
        return;
    }

    if (x < 0) {
        x = 0;
    }
    if (page < 0) {
        page = 0;
    }
    if (x_end > LCD_VISUAL_WIDTH) {
        x_end = LCD_VISUAL_WIDTH;
    }
    if (page_end > LCD_BUFFER_PAGES) {
        page_end = LCD_BUFFER_PAGES;
    }

    for (int dst_page = page; dst_page < page_end; dst_page++) {
        for (int dst_x = x; dst_x < x_end; dst_x++) {
            g_frameBuffer[dst_x / LCD_BUFFER_BLOCK_SIZE][dst_page][dst_x % LCD_BUFFER_BLOCK_SIZE] = 0;
        }
    }
}

void LCD_BufferBlitPageRect(int x, int page, int width, int pages, const uint8_t *bitmap) {
    if (bitmap == NULL || width <= 0 || pages <= 0) {
        return;
    }

    for (int src_page = 0; src_page < pages; src_page++) {
        int dst_page = page + src_page;

        if (dst_page < 0 || dst_page >= LCD_BUFFER_PAGES) {
            continue;
        }

        for (int src_x = 0; src_x < width; src_x++) {
            int dst_x = x + src_x;

            if (dst_x < 0 || dst_x >= LCD_VISUAL_WIDTH) {
                continue;
            }

            g_frameBuffer[dst_x / LCD_BUFFER_BLOCK_SIZE][dst_page][dst_x % LCD_BUFFER_BLOCK_SIZE] =
                bitmap[src_page * width + src_x];
        }
    }
}

void LCD_BufferFill(void) {
    memset(g_frameBuffer, 0xFF, sizeof(g_frameBuffer));
}
