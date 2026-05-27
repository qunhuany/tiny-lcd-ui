# Tiny LCD UI 中文说明

## 项目定位

Tiny LCD UI 是一个面向嵌入式固件的单色 LCD UI 中间层。

它只负责：

- 屏幕缓冲区
- 视觉坐标绘图
- UTF-8 点阵文字绘制
- 字模编辑和固件字库生成工具

它不负责：

- I2C/SPI 通信
- LCD 控制器初始化命令
- DMA/RTOS/互斥锁
- 具体屏幕协议
- 产品菜单和业务逻辑

也就是说，这个项目到 framebuffer 层结束。真正把 framebuffer 写到屏幕上的代码，应该放在下游固件工程里。

相关中文文档：

- [层级说明](LAYERS.md)
- [开源整理说明](OPEN_SOURCE_NOTES.md)

## 层级关系

```text
应用页面代码
    |
    v
UTF-8 文字层
    |
    v
视觉绘图层
    |
    v
屏幕缓冲层
    |
    v
下游屏幕驱动
```

下游屏幕驱动不属于本项目。

## 核心文件

```text
core/lcd.h                 缓冲区尺寸和 framebuffer API
core/lcd.c                 缓冲区存储、视觉坐标到原生布局的映射
core/ui_render.h           绘图接口
core/ui_render.c           点、线、矩形、位图、曲线绘制
core/ui_font.h             UTF-8 字体接口
core/ui_font.c             UTF-8 解码、字形查找、测量、绘制
font/ui_font_generated.h   生成字库声明
font/ui_font_generated.c   生成字模数据
```

## 缓冲区布局

默认屏幕大小是 128x64。

```c
#define LCD_BUFFER_X_BLOCKS 16
#define LCD_BUFFER_PAGES 8
#define LCD_BUFFER_BLOCK_SIZE 8
```

缓冲区是：

```c
uint8_t g_frameBuffer[LCD_BUFFER_X_BLOCKS][LCD_BUFFER_PAGES][LCD_BUFFER_BLOCK_SIZE];
```

绘图层使用常见的左上角视觉坐标：

```text
(0, 0) ----------------> x
  |
  |
  v
  y
```

缓冲区内部仍保留 page-oriented 的 LCD 内存布局，方便下游驱动按自己的屏幕协议上传。

## 最小调用示例

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
    UI_DrawUtf8Text(4, 24, &uiFontDefault, "中文菜单", 0);
}
```

渲染完成后，下游工程读取 `g_frameBuffer`，再用自己的 I2C、SPI 或其它协议写到屏幕。

## 下游上传边界示例

下面的函数不属于本项目，只展示边界应该在哪里。

```c
void uploadFrameBufferToDisplay(void) {
    for (int page = 0; page < LCD_BUFFER_PAGES; page++) {
        for (int block = 0; block < LCD_BUFFER_X_BLOCKS; block++) {
            const uint8_t *bytes = g_frameBuffer[block][page];

            /*
             * 下游工程自己完成：
             * - 设置 LCD page/column
             * - 写入 LCD_BUFFER_BLOCK_SIZE 个字节
             */
        }
    }
}
```

## 字库工具

字体工具位于：

```text
tools/ui/
```

启动方式：

```powershell
python tools\ui\font_tool_main.py
```

典型流程：

1. 加载或编辑字模。
2. 加入 UI 需要的字符。
3. 使用 `tools/ui/unifont.ttf` 生成缺失字形。
4. 导出固件字库。
5. 将生成的 `font/ui_font_generated.*` 编入固件。

