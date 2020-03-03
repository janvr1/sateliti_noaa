from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtCharts import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PIL import Image
import numpy as np
from skimage import filters as skfilt
from skimage import exposure as skexp
from skimage import img_as_ubyte
from scipy import ndimage

from image_processing import *


class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # Setting the image
        self.pixmap_label = QLabel()
        # self.pixmap_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.im_array = np.array([])
        self.cur_im_arr = np.array([])

        self.history = []

        # Gaussian blur slider
        self.gauss_slider = QSlider()
        self.gauss_slider.setOrientation(Qt.Orientation.Horizontal)
        self.gauss_slider.setRange(0, 100)
        self.gauss_slider.valueChanged.connect(self.gaussian_blur)
        self.gauss_label = QLabel("Gaussian blur")
        self.gauss_button = QPushButton("Apply")
        self.gauss_button.clicked.connect(self.apply_changes)

        # Gamma slider
        self.gamma_slider = QSlider()
        self.gamma_slider.setOrientation(Qt.Orientation.Horizontal)
        self.gamma_slider.setRange(1, 100)
        self.gamma_slider.setValue(50)
        self.gamma_slider.valueChanged.connect(self.gamma_correction)
        self.gamma_label = QLabel("Gamma correction")
        self.gamma_button = QPushButton("Apply")
        self.gamma_button.clicked.connect(self.apply_changes)

        # Equalize histogram button
        self.eq_hist_button = QPushButton("Equalize histogram")
        self.eq_hist_button.clicked.connect(self.equalize_histogram)

        # Undo button
        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo)

        # GUI layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.pixmap_label)

        # Histogram
        self.canvas = FigureCanvasQTAgg(Figure(figsize=(5, 3)))
        self._static_ax = self.canvas.figure.subplots()
        self.hist_label = QLabel("Histogram")

        # Right layout
        self.widget_right = QWidget()
        self.widget_right.setMaximumWidth(400)
        self.layout_right = QVBoxLayout()
        self.layout_right.addWidget(self.gauss_label)
        self.layout_right.addWidget(self.gauss_slider)
        self.layout_right.addWidget(self.gauss_button)
        self.layout_right.addWidget(self.gamma_label)
        self.layout_right.addWidget(self.gamma_slider)
        self.layout_right.addWidget(self.gamma_button)
        self.layout_right.addWidget(self.eq_hist_button)
        self.layout_right.addWidget(self.undo_button)
        self.layout_right.addStretch()
        self.layout_right.addWidget(self.hist_label)
        self.layout_right.addWidget(self.canvas)

        self.widget_right.setLayout(self.layout_right)
        self.layout.addWidget(self.widget_right)
        # self.layout.addLayout(self.layout_right)
        self.setLayout(self.layout)

    def new_file_received(self, fname):
        image = load_image(fname)
        self.pixmap_label.setPixmap(image.resize((800, 600)).toqpixmap())
        self.im_array = np.array(image)
        self.cur_im_arr = self.im_array
        self.create_histogram(compute_histogram(self.cur_im_arr))

    def save_current_image(self, fname):
        save_image(fname, self.cur_im_arr)

    @Slot()
    def gaussian_blur(self):
        value = self.gauss_slider.value() / 25
        self.cur_im_arr = gaussian_blur(self.im_array, value)
        self.refresh_pixmap(self.cur_im_arr)
        # image = Image.fromarray(self.cur_im_arr)
        # self.pixmap_label.setPixmap(image.resize((800, 600)).toqpixmap())
        self.gauss_label.setText(f"Gaussian blur: {value}")

    @Slot()
    def gamma_correction(self):
        value = self.gamma_slider.value() / 50
        self.cur_im_arr = gamma_correction(self.im_array, value)
        self.refresh_pixmap(self.cur_im_arr)
        # image = Image.fromarray(self.cur_im_arr)
        # self.pixmap_label.setPixmap(image.resize((800, 600)).toqpixmap())
        self.gamma_label.setText(f"Gamma correction: {value}")

    @Slot()
    def equalize_histogram(self):
        self.cur_im_arr = equalize_histogram(self.im_array)
        self.refresh_pixmap(self.cur_im_arr)
        # image = Image.fromarray(self.cur_im_arr)
        # self.pixmap_label.setPixmap(image.resize((800, 600)).toqpixmap())
        self.apply_changes()

    @Slot()
    def apply_changes(self):
        self.history.append(self.im_array)
        self.im_array = self.cur_im_arr
        self.create_histogram(compute_histogram(self.im_array))

    @Slot()
    def undo(self):
        self.im_array = self.history.pop(0)
        self.refresh_pixmap(self.im_array)
        self.create_histogram(compute_histogram(self.im_array))

    def refresh_pixmap(self, im_arr):
        image = Image.fromarray(im_arr)
        w = self.pixmap_label.width()
        h = self.pixmap_label.height()
        self.pixmap_label.setPixmap(image.resize((800, 600)).toqpixmap())

    def create_histogram(self, histogram):
        self._static_ax.clear()
        bins = histogram[1]
        vals = histogram[0] / np.sum(histogram[0])
        self._static_ax.bar(bins, vals)
        self._static_ax.set_yticklabels([])
        self._static_ax.figure.canvas.draw()

    # def resizeEvent(self, event):
    # print(self.pixmap_label.height())
    # print(self.pixmap_label.width())
    # self.refresh_pixmap(self.cur_im_arr)
