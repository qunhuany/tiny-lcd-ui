from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


UI_DIR = Path(__file__).resolve().parent
SHELLLIB_DIR = UI_DIR.parent
PACKAGE_ROOT = SHELLLIB_DIR.parent
OUTPUT_ROOT = UI_DIR / "output"
DEFAULT_HEADER = OUTPUT_ROOT / "lcd_sim_edited_glyphs.h"
DEFAULT_FONT = UI_DIR / "unifont.ttf"
DEFAULT_OUTPUT_DIR = OUTPUT_ROOT / "font_tool"
DEFAULT_INCLUDE_CHARS_FILES = [
    OUTPUT_ROOT / "cn_ui" / "cn_ui_chars.txt",
    OUTPUT_ROOT / "ru_ui" / "ru_ui_chars.txt",
]
DEFAULT_INCLUDE_TEXT = (
    "LCD FONT OK123.45 mA设置成功中文菜单选择距离校准真实偏移滤波模式稳定快速"
    "Кал.дистФильтрСтаб.Быстр.?%+"
    "StartBASICDISPLAYADVANCESERVICEFACTORY"
    "LLIMHLIMRANGEFILTUnitMModeOUTPUTCALIBALGOSIMISIM"
    "DISTCALSLOPEBIASUARTPKMODEPKDISTPKRELCZTBINRESET"
    "0:DIST1:LEVEL0:STABLE1:FAST0:4-20mA1:20-4mA0:OFF1:ON0:FIRST1:STRONGSIM MAFLTMM"
)
DEFAULT_INC = PACKAGE_ROOT / "font" / "ui_font_generated.h"
DEFAULT_SRC = PACKAGE_ROOT / "font" / "ui_font_generated.c"
DEFAULT_ASCII_Y_SHIFT = -3


@dataclass
class Glyph:
    codepoint: int
    rows: list[int]
    width: int
    height: int
    advance: int
    x_offset: int = 0
    y_offset: int = 0


def parse_int_list(raw: str) -> list[int]:
    return [int(item.strip(), 0) for item in raw.split(",") if item.strip()]


def parse_glyph_header(path: Path) -> dict[int, Glyph]:
    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8", errors="ignore")
    rows_by_name: dict[str, list[int]] = {}
    glyphs: dict[int, Glyph] = {}
    rows_pattern = re.compile(
        r"static\s+const\s+uint16_t\s+(glyph_u[0-9A-Fa-f]+(?:_rows)?)\s*\[\d+\]\s*=\s*\{([^}]*)\}",
        re.S,
    )
    for match in rows_pattern.finditer(text):
        rows_by_name[match.group(1)] = parse_int_list(match.group(2))

    entry_pattern = re.compile(
        r"\{\s*(0x[0-9A-Fa-f]+|\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,"
        r"\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(glyph_u[0-9A-Fa-f]+(?:_rows)?)\s*\}"
    )
    for match in entry_pattern.finditer(text):
        rows = rows_by_name.get(match.group(7), [])
        if rows:
            glyphs[int(match.group(1), 0)] = Glyph(
                codepoint=int(match.group(1), 0),
                width=int(match.group(2)),
                height=int(match.group(3)),
                advance=int(match.group(4)),
                x_offset=int(match.group(5)),
                y_offset=int(match.group(6)),
                rows=rows,
            )

    if glyphs:
        return glyphs

    legacy_pattern = re.compile(
        r"static\s+const\s+uint16_t\s+glyph_u([0-9A-Fa-f]+)\s*\[(\d+)\]\s*=\s*\{([^}]*)\};"
        r"\s*/\*[^*]*width=(\d+)\s+advance=(\d+)\s+y_offset=(-?\d+)",
        re.S,
    )
    for match in legacy_pattern.finditer(text):
        codepoint = int(match.group(1), 16)
        glyphs[codepoint] = Glyph(
            codepoint=codepoint,
            rows=parse_int_list(match.group(3)),
            width=int(match.group(4)),
            height=int(match.group(2)),
            advance=int(match.group(5)),
            y_offset=int(match.group(6)),
        )
    return glyphs


def is_cjk(char: str) -> bool:
    codepoint = ord(char)
    return (
        0x3400 <= codepoint <= 0x4DBF
        or 0x4E00 <= codepoint <= 0x9FFF
        or 0xF900 <= codepoint <= 0xFAFF
    )


def render_ttf_glyph(char: str, font: ImageFont.FreeTypeFont, size: int = 16, threshold: int = 128) -> Glyph:
    if char == " ":
        return Glyph(ord(char), [0], 4, 1, 4, 0, size - 1)

    canvas_size = size * 4
    canvas = Image.new("L", (canvas_size, canvas_size), 255)
    draw = ImageDraw.Draw(canvas)
    bbox = draw.textbbox((0, 0), char, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (canvas_size - text_width) // 2 - bbox[0]
    y = (canvas_size - text_height) // 2 - bbox[1]
    draw.text((x, y), char, font=font, fill=0)

    drawn_bbox = (x + bbox[0], y + bbox[1], x + bbox[2], y + bbox[3])
    if is_cjk(char):
        glyph_width = size
        glyph_height = size
        advance = size
        y_offset = 0
        glyph_img = Image.new("L", (glyph_width, glyph_height), 255)
        if drawn_bbox[2] > drawn_bbox[0] and drawn_bbox[3] > drawn_bbox[1]:
            cropped = canvas.crop(drawn_bbox)
            cropped.thumbnail((glyph_width, glyph_height), Image.Resampling.LANCZOS)
            glyph_img.paste(cropped, ((glyph_width - cropped.width) // 2, (glyph_height - cropped.height) // 2))
    else:
        if drawn_bbox[2] <= drawn_bbox[0] or drawn_bbox[3] <= drawn_bbox[1]:
            return Glyph(ord(char), [0], 4, 1, 4, 0, size - 1)
        cropped = canvas.crop(drawn_bbox)
        cropped = cropped.point(lambda p: 0 if p < threshold else 255)
        bbox2 = cropped.getbbox()
        if bbox2:
            cropped = cropped.crop(bbox2)
        glyph_width = min(size, max(1, cropped.width))
        glyph_height = min(size, max(1, cropped.height))
        glyph_img = Image.new("L", (glyph_width, glyph_height), 255)
        cropped.thumbnail((glyph_width, glyph_height), Image.Resampling.LANCZOS)
        glyph_img.paste(cropped, ((glyph_width - cropped.width) // 2, glyph_height - cropped.height))
        measured_advance = int(round(draw.textlength(char, font=font)))
        advance = max(3, min(size, measured_advance if measured_advance > 0 else glyph_width))
        y_offset = size - glyph_height

    rows: list[int] = []
    for row in range(glyph_height):
        value = 0
        for col in range(glyph_width):
            if glyph_img.getpixel((col, row)) < threshold:
                value |= 1 << (glyph_width - 1 - col)
        rows.append(value)
    return Glyph(ord(char), rows, glyph_width, glyph_height, advance, 0, y_offset)


def add_missing_text_glyphs(
    glyphs: dict[int, Glyph],
    text: str,
    font_path: Path,
    font_size: int,
    threshold: int,
    font_index: int = 0,
) -> list[int]:
    if not text:
        return []
    font = ImageFont.truetype(str(font_path), font_size, index=font_index)
    added: list[int] = []
    for char in text:
        codepoint = ord(char)
        if codepoint not in glyphs:
            glyphs[codepoint] = render_ttf_glyph(char, font, 16, threshold)
            added.append(codepoint)
    return added


def apply_ascii_y_shift(glyphs: dict[int, Glyph], shift: int) -> None:
    if shift == 0:
        return
    for codepoint, glyph in glyphs.items():
        if 0x20 <= codepoint <= 0x7E:
            glyph.y_offset = max(0, min(15, glyph.y_offset + shift))


def read_include_chars_file(path: Path) -> str:
    if not path.exists():
        return ""
    return "".join(ch for ch in path.read_text(encoding="utf-8", errors="ignore") if not ch.isspace())


def format_rows(rows: list[int]) -> str:
    return ", ".join(f"0x{row:04X}" for row in rows)


def edited_glyphs_header(glyphs: dict[int, Glyph]) -> str:
    lines = [
        "#pragma once",
        "#include <stdint.h>",
        "",
        "/* Edited glyphs from ShellLib/ui.",
        " * Visual rows: row 0 is top, highest bit is left.",
        " * UiGlyph entries carry layout metrics for multilingual variable-width text.",
        " */",
        "",
        "typedef struct {",
        "    uint32_t codepoint;",
        "    uint8_t width;",
        "    uint8_t height;",
        "    uint8_t advance;",
        "    int8_t x_offset;",
        "    int8_t y_offset;",
        "    const uint16_t *rows;",
        "} UiGlyph;",
        "",
    ]
    for codepoint in sorted(glyphs):
        glyph = glyphs[codepoint]
        lines.append(
            f"static const uint16_t glyph_u{codepoint:04X}_rows[{glyph.height}] = "
            f"{{ {format_rows(glyph.rows)} }}; /* U+{codepoint:04X} */"
        )
    lines.extend(["", "static const UiGlyph uiFontGlyphs[] = {"])
    for codepoint in sorted(glyphs):
        glyph = glyphs[codepoint]
        lines.append(
            f"    {{ 0x{codepoint:04X}, {glyph.width}, {glyph.height}, {glyph.advance}, "
            f"{glyph.x_offset}, {glyph.y_offset}, glyph_u{codepoint:04X}_rows }},"
        )
    lines.extend(
        [
            "};",
            "",
            "static const uint16_t uiFontGlyphsCount = sizeof(uiFontGlyphs) / sizeof(uiFontGlyphs[0]);",
            "",
        ]
    )
    return "\n".join(lines)


def firmware_header() -> str:
    return "\n".join(
        [
            "#ifndef UI_FONT_GENERATED_H",
            "#define UI_FONT_GENERATED_H",
            "",
            "#include <stdint.h>",
            "",
            '#include "ui_font.h"',
            "",
            "extern const UiGlyph uiFontGlyphs[];",
            "extern const uint16_t uiFontGlyphsCount;",
            "extern const UiFont uiFontDefault;",
            "",
            "#endif // UI_FONT_GENERATED_H",
            "",
        ]
    )


def firmware_source(glyphs: dict[int, Glyph]) -> str:
    lines: list[str] = [
        '#include "ui_font_generated.h"',
        "",
        "/* Auto-generated from ShellLib/ui edited glyphs.",
        " * Visual rows: row 0 is top, highest bit is left.",
        " */",
        "",
    ]
    for codepoint in sorted(glyphs):
        glyph = glyphs[codepoint]
        lines.append(
            f"static const uint16_t glyph_u{codepoint:04X}_rows[{glyph.height}] = "
            f"{{ {format_rows(glyph.rows)} }}; /* U+{codepoint:04X} */"
        )
    lines.extend(["", "const UiGlyph uiFontGlyphs[] = {"])
    for codepoint in sorted(glyphs):
        glyph = glyphs[codepoint]
        lines.append(
            f"    {{ 0x{codepoint:04X}, {glyph.width}, {glyph.height}, {glyph.advance}, "
            f"{glyph.x_offset}, {glyph.y_offset}, glyph_u{codepoint:04X}_rows }},"
        )
    lines.extend(
        [
            "};",
            "",
            "const uint16_t uiFontGlyphsCount = (uint16_t)(sizeof(uiFontGlyphs) / sizeof(uiFontGlyphs[0]));",
            "",
            "const UiFont uiFontDefault = {",
            "    uiFontGlyphs,",
            "    (uint16_t)(sizeof(uiFontGlyphs) / sizeof(uiFontGlyphs[0])),",
            "    16",
            "};",
            "",
        ]
    )
    return "\n".join(lines)
