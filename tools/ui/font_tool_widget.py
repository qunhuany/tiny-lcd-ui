from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QColor, QImage, QMouseEvent, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QSizePolicy,
    QWidget,
)

try:
    from .font_backend import (
        DEFAULT_ASCII_Y_SHIFT,
        DEFAULT_FONT,
        DEFAULT_HEADER,
        DEFAULT_INC,
        DEFAULT_INCLUDE_CHARS_FILES,
        DEFAULT_INCLUDE_TEXT,
        DEFAULT_OUTPUT_DIR,
        DEFAULT_SRC,
        add_missing_text_glyphs,
        apply_ascii_y_shift,
        edited_glyphs_header,
        firmware_header,
        firmware_source,
        parse_glyph_header,
        read_include_chars_file,
        render_ttf_glyph,
    )
    from .ui_font_tool import Ui_FontToolWidget
except ImportError:
    from font_backend import (
        DEFAULT_ASCII_Y_SHIFT,
        DEFAULT_FONT,
        DEFAULT_HEADER,
        DEFAULT_INC,
        DEFAULT_INCLUDE_CHARS_FILES,
        DEFAULT_INCLUDE_TEXT,
        DEFAULT_OUTPUT_DIR,
        DEFAULT_SRC,
        add_missing_text_glyphs,
        apply_ascii_y_shift,
        edited_glyphs_header,
        firmware_header,
        firmware_source,
        parse_glyph_header,
        read_include_chars_file,
        render_ttf_glyph,
    )
    from ui_font_tool import Ui_FontToolWidget


UI_DIR = Path(__file__).resolve().parent
SCRIPT_DIR = UI_DIR.parent
DEFAULT_CHARSET = "基础设置距离校准显示语言0123456789.mA%+-"


@dataclass
class DisplayConfig:
    width: int = 128
    height: int = 64
    page_height: int = 8


class GlyphGridWidget(QWidget):
    glyphEdited = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.glyph = None
        self.cell = 12
        self.setMinimumSize(260, 260)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_glyph(self, glyph) -> None:
        self.glyph = glyph
        self.updateGeometry()
        self.update()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("white"))
        if self.glyph is None:
            painter.setPen(QColor(80, 80, 80))
            painter.drawText(self.rect(), Qt.AlignCenter, "No glyph")
            return

        width = max(1, int(self.glyph.width))
        height = max(1, int(self.glyph.height))
        cell = max(4, min(self.width() // width, self.height() // height))
        self.cell = cell
        grid_w = width * cell
        grid_h = height * cell
        x0 = (self.width() - grid_w) // 2
        y0 = (self.height() - grid_h) // 2

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("black"))
        for row_idx, row_bits in enumerate(self.glyph.rows[:height]):
            for col in range(width):
                if row_bits & (1 << (width - 1 - col)):
                    painter.drawRect(x0 + col * cell, y0 + row_idx * cell, cell, cell)

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(210, 210, 210), 1))
        for col in range(width + 1):
            x = x0 + col * cell
            painter.drawLine(x, y0, x, y0 + grid_h)
        for row in range(height + 1):
            y = y0 + row * cell
            painter.drawLine(x0, y, x0 + grid_w, y)
        painter.setPen(QPen(QColor(70, 130, 180), 2))
        painter.drawRect(x0, y0, grid_w, grid_h)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.toggle_at(event.position().toPoint())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.LeftButton:
            self.toggle_at(event.position().toPoint(), draw_only=True)

    def toggle_at(self, point: QPoint, draw_only: bool = False) -> None:
        if self.glyph is None:
            return
        width = max(1, int(self.glyph.width))
        height = max(1, int(self.glyph.height))
        cell = max(4, min(self.width() // width, self.height() // height))
        x0 = (self.width() - width * cell) // 2
        y0 = (self.height() - height * cell) // 2
        col = (point.x() - x0) // cell
        row = (point.y() - y0) // cell
        if row < 0 or row >= height or col < 0 or col >= width:
            return
        ensure_rows(self.glyph)
        mask = 1 << (width - 1 - col)
        if draw_only:
            self.glyph.rows[row] |= mask
        else:
            self.glyph.rows[row] ^= mask
        self.glyphEdited.emit()
        self.update()


class FontToolWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_FontToolWidget()
        self.ui.setupUi(self)

        self.glyphs = {}
        self.original_glyphs = {}
        self.current_codepoint: int | None = None
        self.current_glyph = None
        self.current_image: Image.Image | None = None
        self.updating_fields = False
        self.font_path = DEFAULT_FONT
        self.glyph_store_path = DEFAULT_HEADER
        self.output_dir = DEFAULT_OUTPUT_DIR
        self.glyph_grid = GlyphGridWidget(self)

        self.install_glyph_grid()
        self.init_defaults()
        self.connect_signals()
        self.load_project()

    def install_glyph_grid(self) -> None:
        old = self.ui.glyphPreviewLabel
        layout = old.parentWidget().layout()
        if layout is not None:
            layout.replaceWidget(old, self.glyph_grid)
        old.hide()
        self.glyph_grid.glyphEdited.connect(self.on_glyph_edited)

    def init_defaults(self) -> None:
        self.set_path_display("font", self.font_path)
        self.set_path_display("glyph", self.glyph_store_path)
        self.set_path_display("output", self.output_dir)
        self.ui.charsetTextEdit.setPlainText(DEFAULT_CHARSET)
        self.ui.previewTextEdit.setPlainText("基础设置\n距离校准\n12.345mA")
        self.ui.glyphInputEdit.setText("基")
        self.set_preview_text("Enter preview text and load a glyph.")

    def connect_signals(self) -> None:
        self.ui.loadProjectButton.clicked.connect(self.load_project)
        self.ui.applyCharsetButton.clicked.connect(self.apply_charset)
        self.ui.loadCharsetFileButton.clicked.connect(self.load_charset_file)
        self.ui.glyphInputEdit.returnPressed.connect(self.load_input_glyph)
        self.ui.glyphInputEdit.textChanged.connect(self.load_input_glyph)
        self.ui.loadGlyphButton.clicked.connect(self.load_input_glyph)
        self.ui.previewTextEdit.textChanged.connect(self.refresh_preview)
        self.ui.zoomSlider.valueChanged.connect(self.refresh_preview)
        self.ui.lcdWidthSpinBox.valueChanged.connect(self.refresh_preview)
        self.ui.lcdHeightSpinBox.valueChanged.connect(self.refresh_preview)
        self.ui.fontSizeSpinBox.valueChanged.connect(self.regenerate_current_glyph)
        self.ui.thresholdSpinBox.valueChanged.connect(self.regenerate_current_glyph)
        self.ui.showGridCheckBox.stateChanged.connect(self.refresh_preview)
        self.ui.showPageGridCheckBox.stateChanged.connect(self.refresh_preview)
        self.ui.shiftGlyphUpButton.clicked.connect(lambda: self.shift_current_glyph(0, -1))
        self.ui.shiftGlyphDownButton.clicked.connect(lambda: self.shift_current_glyph(0, 1))
        self.ui.shiftGlyphLeftButton.clicked.connect(lambda: self.shift_current_glyph(-1, 0))
        self.ui.shiftGlyphRightButton.clicked.connect(lambda: self.shift_current_glyph(1, 0))
        self.ui.clearGlyphButton.clicked.connect(self.clear_current_glyph)
        self.ui.applyGlyphMetricButton.clicked.connect(self.apply_metrics)
        self.ui.glyphWidthSpinBox.valueChanged.connect(self.apply_metrics)
        self.ui.glyphHeightSpinBox.valueChanged.connect(self.apply_metrics)
        self.ui.glyphAdvanceSpinBox.valueChanged.connect(self.apply_metrics)
        self.ui.glyphXOffsetSpinBox.valueChanged.connect(self.apply_metrics)
        self.ui.glyphYOffsetSpinBox.valueChanged.connect(self.apply_metrics)
        self.ui.resetGlyphButton.clicked.connect(self.reset_current_glyph)
        self.ui.regenerateGlyphButton.clicked.connect(self.regenerate_current_glyph)
        self.ui.saveGlyphButton.clicked.connect(self.save_current_glyph)
        self.ui.browseFontButton.clicked.connect(self.browse_font)
        self.ui.browseGlyphStoreButton.clicked.connect(self.browse_glyph_store)
        self.ui.browseOutputDirButton.clicked.connect(self.browse_output_dir)
        self.ui.validateAllButton.clicked.connect(self.validate_all)
        self.ui.generateMissingGlyphsButton.clicked.connect(self.generate_missing_glyphs)
        self.ui.exportFirmwareFontButton.clicked.connect(self.export_firmware_font)

    def display_config(self) -> DisplayConfig:
        return DisplayConfig(
            width=self.ui.lcdWidthSpinBox.value(),
            height=self.ui.lcdHeightSpinBox.value(),
        )

    def load_project(self) -> None:
        glyph_path = self.glyph_store_path
        self.glyphs = parse_glyph_header(glyph_path)
        self.original_glyphs = copy.deepcopy(self.glyphs)
        self.append_log(f"Loaded {len(self.glyphs)} glyphs from {glyph_path}")
        self.apply_charset()
        self.load_input_glyph()
        self.refresh_preview()

    def apply_charset(self) -> None:
        chars = self.charset_chars()
        self.ui.charsetSummaryLabel.setText(f"{len(chars)} chars")
        self.append_log(f"Charset applied: {len(chars)} unique chars")

    def load_charset_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Load charset text", str(SCRIPT_DIR), "Text files (*.txt *.md);;All files (*.*)")
        if not path:
            return
        self.ui.charsetTextEdit.setPlainText(Path(path).read_text(encoding="utf-8", errors="ignore"))
        self.apply_charset()

    def load_input_glyph(self) -> None:
        text = self.ui.glyphInputEdit.text()
        ch = next((item for item in text if not item.isspace()), "")
        if not ch:
            return
        self.load_glyph(ch)

    def load_glyph(self, ch: str) -> None:
        codepoint = ord(ch)
        glyph = self.glyphs.get(codepoint)
        source = "existing"
        if glyph is None:
            glyph = self.generate_glyph(ch)
            self.glyphs[codepoint] = glyph
            source = "generated"
        self.current_codepoint = codepoint
        self.current_glyph = glyph
        self.ui.glyphCodepointEdit.setText(f"U+{codepoint:04X}")
        self.ui.glyphSourceEdit.setText(source if glyph is not None else "missing")
        self.glyph_grid.set_glyph(glyph)
        self.update_glyph_fields()
        self.refresh_preview()

    def generate_glyph(self, ch: str):
        font = ImageFont.truetype(str(self.font_path), self.ui.fontSizeSpinBox.value(), index=0)
        return render_ttf_glyph(ch, font, self.ui.fontSizeSpinBox.value(), self.ui.thresholdSpinBox.value())

    def update_glyph_fields(self) -> None:
        glyph = self.current_glyph
        if glyph is None:
            self.ui.glyphRowsEdit.clear()
            return
        self.updating_fields = True
        self.ui.glyphWidthSpinBox.setValue(glyph.width)
        self.ui.glyphHeightSpinBox.setValue(glyph.height)
        self.ui.glyphAdvanceSpinBox.setValue(glyph.advance)
        self.ui.glyphXOffsetSpinBox.setValue(glyph.x_offset)
        self.ui.glyphYOffsetSpinBox.setValue(glyph.y_offset)
        self.updating_fields = False
        self.update_rows_edit()

    def update_rows_edit(self) -> None:
        if self.current_glyph is None:
            self.ui.glyphRowsEdit.clear()
            return
        self.ui.glyphRowsEdit.setPlainText(", ".join(f"0x{row:04X}" for row in self.current_glyph.rows))

    def on_glyph_edited(self) -> None:
        self.update_rows_edit()
        self.refresh_preview()

    def apply_metrics(self) -> None:
        if self.updating_fields:
            return
        glyph = self.current_glyph
        if glyph is None:
            return
        glyph.width = self.ui.glyphWidthSpinBox.value()
        glyph.height = self.ui.glyphHeightSpinBox.value()
        glyph.advance = self.ui.glyphAdvanceSpinBox.value()
        glyph.x_offset = self.ui.glyphXOffsetSpinBox.value()
        glyph.y_offset = self.ui.glyphYOffsetSpinBox.value()
        ensure_rows(glyph)
        mask = (1 << glyph.width) - 1
        glyph.rows = [row & mask for row in glyph.rows[: glyph.height]]
        self.glyph_grid.update()
        self.update_rows_edit()
        self.refresh_preview()

    def shift_current_glyph(self, dx: int, dy: int) -> None:
        glyph = self.current_glyph
        if glyph is None:
            return
        ensure_rows(glyph)
        width = glyph.width
        mask = (1 << width) - 1
        if dx < 0:
            glyph.rows = [((row << 1) & mask) for row in glyph.rows]
        elif dx > 0:
            glyph.rows = [(row >> 1) for row in glyph.rows]
        if dy < 0:
            glyph.rows = glyph.rows[1:] + [0]
        elif dy > 0:
            glyph.rows = [0] + glyph.rows[:-1]
        self.on_glyph_edited()
        self.glyph_grid.update()

    def clear_current_glyph(self) -> None:
        if self.current_glyph is None:
            return
        self.current_glyph.rows = [0 for _ in range(self.current_glyph.height)]
        self.on_glyph_edited()
        self.glyph_grid.update()

    def reset_current_glyph(self) -> None:
        if self.current_codepoint is None:
            return
        original = self.original_glyphs.get(self.current_codepoint)
        if original is None:
            return
        self.glyphs[self.current_codepoint] = copy.deepcopy(original)
        self.current_glyph = self.glyphs[self.current_codepoint]
        self.glyph_grid.set_glyph(self.current_glyph)
        self.update_glyph_fields()
        self.refresh_preview()

    def regenerate_current_glyph(self) -> None:
        if self.updating_fields:
            return
        if self.current_codepoint is None:
            return
        ch = chr(self.current_codepoint)
        self.current_glyph = self.generate_glyph(ch)
        self.glyphs[self.current_codepoint] = self.current_glyph
        self.glyph_grid.set_glyph(self.current_glyph)
        self.update_glyph_fields()
        self.refresh_preview()

    def save_current_glyph(self) -> None:
        if self.current_codepoint is None or self.current_glyph is None:
            return
        self.glyphs[self.current_codepoint] = self.current_glyph
        self.append_log(f"Saved glyph U+{self.current_codepoint:04X}")

    def generate_missing_glyphs(self) -> None:
        chars = self.charset_chars()
        added = []
        for ch in chars:
            codepoint = ord(ch)
            if codepoint in self.glyphs:
                continue
            self.glyphs[codepoint] = self.generate_glyph(ch)
            added.append(codepoint)

        self.append_log(f"Generated {len(added)} missing glyphs from charset")
        if added:
            self.append_log("Added: " + ", ".join(f"U+{codepoint:04X}" for codepoint in added))
        self.load_input_glyph()
        self.refresh_preview()

    def export_firmware_font(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        edited_header = self.output_dir / "lcd_sim_edited_glyphs.h"
        self.generate_missing_glyphs()
        edited_header.write_text(edited_glyphs_header(self.glyphs), encoding="utf-8")
        self.glyph_store_path = edited_header
        self.set_path_display("glyph", self.glyph_store_path)

        export_glyphs = copy.deepcopy(self.glyphs)
        include_text = DEFAULT_INCLUDE_TEXT + "".join(self.charset_chars())
        include_text += self.ui.previewTextEdit.toPlainText()
        for include_chars_file in DEFAULT_INCLUDE_CHARS_FILES:
            include_text += read_include_chars_file(include_chars_file)

        added = add_missing_text_glyphs(
            export_glyphs,
            include_text,
            self.font_path,
            self.ui.fontSizeSpinBox.value(),
            self.ui.thresholdSpinBox.value(),
            0,
        )
        apply_ascii_y_shift(export_glyphs, DEFAULT_ASCII_Y_SHIFT)

        DEFAULT_INC.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_SRC.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_INC.write_text(firmware_header(), encoding="utf-8")
        DEFAULT_SRC.write_text(firmware_source(export_glyphs), encoding="utf-8")

        self.append_log(f"Saved edited glyphs: {edited_header}")
        self.append_log(f"Exported firmware font: {len(export_glyphs)} glyphs")
        if added:
            self.append_log("Firmware added: " + ", ".join(f"U+{codepoint:04X}" for codepoint in added))
        self.append_log(f"Header: {DEFAULT_INC}")
        self.append_log(f"Source: {DEFAULT_SRC}")

    def refresh_preview(self) -> None:
        img = render_string_preview(self.ui.previewTextEdit.toPlainText(), self.glyphs, self.display_config())
        self.current_image = img
        self.ui.lcdPreviewLabel.setPixmap(pil_to_pixmap(self.make_preview_image(img)))

    def make_preview_image(self, image: Image.Image) -> Image.Image:
        config = self.display_config()
        scale = self.zoom_scale()
        preview = image.convert("RGB").resize((int(config.width * scale), int(config.height * scale)), Image.Resampling.NEAREST)
        draw = ImageDraw.Draw(preview)
        if self.ui.showGridCheckBox.isChecked() and scale >= 4:
            for x in range(config.width + 1):
                draw.line((x * scale, 0, x * scale, config.height * scale), fill=(225, 225, 225))
            for y in range(config.height + 1):
                draw.line((0, y * scale, config.width * scale, y * scale), fill=(225, 225, 225))
        if self.ui.showPageGridCheckBox.isChecked():
            for y in range(0, config.height + 1, max(1, config.page_height)):
                draw.line((0, y * scale, config.width * scale, y * scale), fill=(80, 160, 220))
        return preview

    def zoom_scale(self) -> float:
        value = self.ui.zoomSlider.value()
        return value / 10.0 if value > 12 else float(value)

    def validate_all(self) -> None:
        chars = set(self.charset_chars())
        missing = sorted(ch for ch in chars if ord(ch) not in self.glyphs)
        clipped = self.collect_preview_clipping_issues()
        self.append_log(
            f"Validation: charset={len(chars)}, glyphs={len(self.glyphs)}, "
            f"missing={len(missing)}, clipped={len(clipped)}"
        )
        if missing:
            self.append_log("Missing: " + "".join(missing))
        if clipped:
            self.append_log("Clipped: " + "; ".join(clipped[:8]))

    def collect_preview_clipping_issues(self) -> list[str]:
        config = self.display_config()
        issues: list[str] = []
        line_y = 0
        for line in self.ui.previewTextEdit.toPlainText().splitlines() or [""]:
            cursor_x = 0
            for ch in line:
                if ch == " ":
                    cursor_x += 4
                    continue
                glyph = self.glyphs.get(ord(ch))
                if glyph is None:
                    cursor_x += 8
                    continue
                x0 = cursor_x + glyph.x_offset
                y0 = line_y + glyph.y_offset
                if x0 < 0 or y0 < 0 or x0 + glyph.width > config.width or y0 + glyph.height > config.height:
                    issues.append(f"{ch}/U+{ord(ch):04X}@({x0},{y0},{glyph.width}x{glyph.height})")
                cursor_x += glyph.advance
            line_y += 16
            if line_y >= config.height:
                break
        return issues

    def browse_font(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select font", str(SCRIPT_DIR), "Fonts (*.ttf *.ttc);;All files (*.*)")
        if path:
            self.font_path = Path(path)
            self.set_path_display("font", self.font_path)

    def browse_glyph_store(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select glyph store", str(SCRIPT_DIR), "C/C++ files (*.h *.c);;All files (*.*)")
        if path:
            self.glyph_store_path = Path(path)
            self.set_path_display("glyph", self.glyph_store_path)

    def browse_output_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select output directory", str(DEFAULT_OUTPUT_DIR))
        if path:
            self.output_dir = Path(path)
            self.set_path_display("output", self.output_dir)

    def set_preview_text(self, text: str) -> None:
        self.ui.lcdPreviewLabel.setText(text)

    def append_log(self, text: str) -> None:
        self.ui.logTextEdit.append(text)

    def set_path_display(self, kind: str, path: Path) -> None:
        label_names = {
            "font": "fontPathValueLabel",
            "glyph": "glyphStorePathValueLabel",
            "output": "outputDirValueLabel",
        }
        label = getattr(self.ui, label_names[kind])
        label.setText(compact_path_label(path))
        label.setToolTip(str(path))

    def charset_chars(self) -> list[str]:
        return sorted({ch for ch in self.ui.charsetTextEdit.toPlainText() if not ch.isspace()})


def ensure_rows(glyph) -> None:
    if len(glyph.rows) < glyph.height:
        glyph.rows = list(glyph.rows) + [0] * (glyph.height - len(glyph.rows))


def compact_path_label(path: Path) -> str:
    if path.is_dir():
        return path.name or str(path)
    parent = path.parent.name
    if parent:
        return f"{parent}/{path.name}"
    return path.name or str(path)


def draw_glyph_to_image(img: Image.Image, glyph, x: int, y: int) -> int:
    if glyph is None:
        return 8
    width = glyph.width
    height = glyph.height
    x0 = x + glyph.x_offset
    y0 = y + glyph.y_offset
    for row_idx, row_bits in enumerate(glyph.rows[:height]):
        for col in range(width):
            if row_bits & (1 << (width - 1 - col)):
                px = x0 + col
                py = y0 + row_idx
                if 0 <= px < img.width and 0 <= py < img.height:
                    img.putpixel((px, py), 0)
    return glyph.advance


def render_string_preview(text: str, glyphs: dict[int, object], config: DisplayConfig) -> Image.Image:
    img = Image.new("1", (config.width, config.height), 1)
    line_y = 0
    for line in text.splitlines() or [""]:
        cursor_x = 0
        for ch in line:
            if ch == " ":
                cursor_x += 4
                continue
            cursor_x += draw_glyph_to_image(img, glyphs.get(ord(ch)), cursor_x, line_y)
        line_y += 16
        if line_y >= config.height:
            break
    return img


def pil_to_pixmap(image: Image.Image) -> QPixmap:
    rgb = image.convert("RGB")
    data = rgb.tobytes("raw", "RGB")
    qimage = QImage(data, rgb.width, rgb.height, rgb.width * 3, QImage.Format_RGB888).copy()
    return QPixmap.fromImage(qimage)
