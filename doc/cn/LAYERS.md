# LCD UI 层级说明

## 1. 屏幕缓冲层

文件：

- `core/lcd.h`
- `core/lcd.c`

职责：

- 使用 `g_frameBuffer` 保存目标画面。
- 将视觉坐标转换为 LCD 原生 page/bit 布局。
- 只保存绘制结果，不包含任何硬件传输逻辑。

耦合情况：

- 不依赖硬件传输。
- 不依赖 STM32 HAL、RTOS、I2C 或 SPI。

该层是本项目的最底层。真正把 framebuffer 写到屏幕上的代码应由下游工程实现。

## 2. 视觉绘图层

文件：

- `core/ui_render.h`
- `core/ui_render.c`

职责：

- 绘制像素、横线、竖线、矩形、填充矩形和清除矩形。
- 绘制 bitmap rows。
- 绘制 8x8 和 16x16 字形位图。
- 绘制简单的 range profile 曲线。

耦合情况：

- 调用 `LCD_BufferSetVisualPixel()` 写入缓冲层。
- 不依赖硬件和 CMSIS。

## 3. 文字和字形层

文件：

- `core/ui_font.h`
- `core/ui_font.c`
- `font/ui_font_generated.h`
- `font/ui_font_generated.c`

职责：

- 解码 UTF-8 文本。
- 按 Unicode codepoint 查找字形。
- 通过视觉绘图层绘制字形。
- 测量 UTF-8 文本宽度。
- 缺字时尝试回退到 `?`。

生成字形结构：

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

## 4. 旧字体路径

无。

旧的 ASCII/数字绘制路径已经移除。本项目只保留 UTF-8 文字接口。

## 5. 工具层

文件：

- `tools/ui/*`
- `tools/output/*`

职责：

- 编辑和生成字形数据。
- 导出固件 C 字库文件。
- 保存共享字符集和字形输出文件。

