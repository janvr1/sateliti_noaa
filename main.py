#!/usr/bin/env python3

import sys

from PySide2.QtWidgets import QApplication

from main_widget import MainWidget
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication()
    # app.setStyle('gtk')

    widget = MainWidget()
    window = MainWindow(widget)

    window.show()

    sys.exit(app.exec_())
