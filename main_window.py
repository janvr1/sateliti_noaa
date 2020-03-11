from PySide2.QtCore import Slot
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog


class MainWindow(QMainWindow):

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
        save_A_action = QAction("Save image A", self)
        # save_A_action.setShortcut("Ctrl+S")
        save_A_action.triggered.connect(self.save_file_A)
        self.file_menu.addAction(save_A_action)

        save_B_action = QAction("Save image B", self)
        save_B_action.triggered.connect(self.save_file_B)
        self.file_menu.addAction(save_B_action)

        save_AB_action = QAction("Save combined image", self)
        save_AB_action.triggered.connect(self.save_file_AB)
        self.file_menu.addAction(save_AB_action)

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
        file_name = dialog.getOpenFileName()[0]
        # print(self.file_name)
        self.status.showMessage(file_name)

        self.centralWidget().new_file_received(file_name)

    @Slot()
    def save_file_A(self):
        # Create file picker dialog
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        # Get file name
        file_name = dialog.getSaveFileName()[0]
        print(file_name)

        self.centralWidget().save_image_A(file_name)

    @Slot()
    def save_file_B(self):
        # Create file picker dialog
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        # Get file name
        file_name = dialog.getSaveFileName()[0]
        print(file_name)

        self.centralWidget().save_image_B(file_name)

    @Slot()
    def save_file_AB(self):
        # Create file picker dialog
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        # Get file name
        file_name = dialog.getSaveFileName()[0]
        print(file_name)

        self.centralWidget().save_image_AB(file_name)
