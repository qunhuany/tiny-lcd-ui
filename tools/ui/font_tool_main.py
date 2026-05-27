from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

try:
    from .font_tool_widget import FontToolWidget
except ImportError:
    from font_tool_widget import FontToolWidget


def main() -> int:
    app = QApplication(sys.argv)
    widget = FontToolWidget()
    widget.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
