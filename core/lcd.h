#ifndef LCD_H
#define LCD_H

#include <stdbool.h>
#include <stdint.h>

#define LCD_BUFFER_X_BLOCKS 16
#define LCD_BUFFER_PAGES 8
#define LCD_BUFFER_BLOCK_SIZE 8
#define LCD_VISUAL_WIDTH (LCD_BUFFER_X_BLOCKS * LCD_BUFFER_BLOCK_SIZE)
#define LCD_VISUAL_HEIGHT (LCD_BUFFER_PAGES * LCD_BUFFER_BLOCK_SIZE)

extern uint8_t g_frameBuffer[LCD_BUFFER_X_BLOCKS][LCD_BUFFER_PAGES][LCD_BUFFER_BLOCK_SIZE];

void LCD_BufferInit(void);
void LCD_BufferClear(void);
void LCD_BufferFill(void);

// Native coordinates match the page-oriented LCD memory layout.
void LCD_BufferSetNativePixel(int rawX, int page, int bit, bool on);

// Visual coordinates use the usual top-left origin expected by drawing code.
void LCD_BufferSetVisualPixel(int x, int y, bool on);

void LCD_BufferClearPageRect(int x, int page, int width, int pages);
void LCD_BufferBlitPageRect(int x, int page, int width, int pages, const uint8_t *bitmap);

#endif // LCD_H
