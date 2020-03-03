from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *


class MainWindow(QMainWindow):
    new_file_signal = Signal(str)

    def __init__(self, widget):
        QMainWindow.__init__(self)
        # Set window title
        self.setWindowTitle("NOAA APT image editor")

        # Set the main widget
        self.setCentralWidget(widget)

        # Add top menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Load file
        load_action = QAction("Load", self)
        load_action.setShortcut("Ctrl+O")

        load_action.triggered.connect(self.load_file)
        self.file_menu.addAction(load_action)

        # Save file
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        self.file_menu.addAction(save_action)

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        # Status bar
        self.status = self.statusBar()
        self.status.showMessage("Hello!")

    @Slot()
    def load_file(self):
        # Create file picker dialog
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)

        # Get file name
        self.file_name = dialog.getOpenFileName()[0]
        # print(self.file_name)
        self.status.showMessage(self.file_name)

        self.centralWidget().new_file_received(self.file_name)

    @Slot()
    def save_file(self):
        # Create file picker dialog
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        # Get file name
        file_name = dialog.getSaveFileName()[0]
        print(file_name)

        self.centralWidget().save_current_image(file_name)
