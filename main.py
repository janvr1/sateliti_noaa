import sys

from PySide2.QtWidgets import QApplication, QStyle
from PySide2.QtCore import *

from main_window import MainWindow
from main_widget import MainWidget

if __name__ == "__main__":
    app = QApplication()
    # app.setStyle('gtk')

    widget = MainWidget()
    window = MainWindow(widget)

    window.show()

    sys.exit(app.exec_())
