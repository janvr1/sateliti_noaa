from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from image_processing import *


class MainWidget(QWidget):
    imA = 0
    imB = 1

    def __init__(self):
        QWidget.__init__(self)

        # Image arrays
        self.im_array_A = np.array([])
        self.im_array_B = np.array([])
        self.cur_im_arr = np.array([])

        self.active = None

        # Pixmap labels
        self.label_A = QLabel("Image A")
        self.pixmapA_label = QLabel()
        self.label_B = QLabel("Image B")
        self.pixmapB_label = QLabel()

        self.layout_A = QVBoxLayout()
        self.layout_A.addWidget(self.label_A)
        self.layout_A.addWidget(self.pixmapA_label)

        self.layout_B = QVBoxLayout()
        self.layout_B.addWidget(self.label_B)
        self.layout_B.addWidget(self.pixmapB_label)

        # Active image picker
        self.label_AB = QLabel("Select active image")
        self.label_AB.setMinimumWidth(400)
        self.radio_A = QRadioButton("A")
        self.radio_B = QRadioButton("B")
        self.radio_A.clicked.connect(self.set_active_A)
        self.radio_B.clicked.connect(self.set_active_B)
        self.layout_radio = QHBoxLayout()
        self.layout_radio.addWidget(self.radio_A)
        self.layout_radio.addWidget(self.radio_B)

        # Gaussian blur slider
        self.gauss_slider = QSlider()
        self.gauss_slider.setOrientation(Qt.Orientation.Horizontal)
        self.gauss_slider.setRange(0, 10)
        self.gauss_slider.valueChanged.connect(self.gaussian_blur)
        self.gauss_label = QLabel("Gaussian blur")
        self.gauss_button = QPushButton("Apply")
        self.gauss_button.clicked.connect(self.apply_changes)

        self.gauss_layout = QHBoxLayout()
        self.gauss_layout.addWidget(self.gauss_slider)
        self.gauss_layout.addWidget(self.gauss_button)

        # Gamma slider
        self.gamma_slider = QSlider()
        self.gamma_slider.setOrientation(Qt.Orientation.Horizontal)
        self.gamma_slider.setRange(1, 9)
        self.gamma_slider.setValue(5)
        self.gamma_slider.valueChanged.connect(self.gamma_correction)
        self.gamma_label = QLabel("Gamma correction")
        self.gamma_button = QPushButton("Apply")
        self.gamma_button.clicked.connect(self.apply_changes)

        self.gamma_layout = QHBoxLayout()
        self.gamma_layout.addWidget(self.gamma_slider)
        self.gamma_layout.addWidget(self.gamma_button)

        # Equalize histogram button
        self.eq_hist_button = QPushButton("Equalize histogram")
        self.eq_hist_button.clicked.connect(self.equalize_histogram)

        # Median filter
        self.median_button = QPushButton("Median filter")
        self.median_button.clicked.connect(self.median_filter)

        # Colorize button
        self.sharpen_button = QPushButton("Sharpen")
        self.sharpen_button.clicked.connect(self.sharpen)

        # Undo button
        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo)
        self.history_A = []
        self.history_B = []

        # Histogram
        self.canvas = FigureCanvasQTAgg(Figure(figsize=(5, 3)))
        self._static_ax = self.canvas.figure.subplots()
        self.hist_label = QLabel("Histogram")

        # Right layout
        self.layout_right = QVBoxLayout()
        self.layout_right.addWidget(self.label_AB)
        self.layout_right.addLayout(self.layout_radio)

        self.layout_right.addWidget(self.gauss_label)
        self.layout_right.addLayout(self.gauss_layout)

        self.layout_right.addWidget(self.gamma_label)
        self.layout_right.addLayout(self.gamma_layout)

        self.layout_right.addWidget(self.eq_hist_button)
        self.layout_right.addWidget(self.median_button)
        self.layout_right.addWidget(self.sharpen_button)

        self.layout_right.addWidget(self.undo_button)
        self.layout_right.addStretch()
        self.layout_right.addWidget(self.hist_label)
        self.layout_right.addWidget(self.canvas)

        # GUI layout
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.layout_A)
        self.layout.addLayout(self.layout_B)
        self.layout.addLayout(self.layout_right)

        self.setLayout(self.layout)

    def new_file_received(self, fname):
        self.im_array_A, self.im_array_B = load_image(fname)
        self.history_A.clear()
        self.history_B.clear()

        self.gamma_slider.setValue(5)
        self.gauss_slider.setValue(0)

        image_A = Image.fromarray(self.im_array_A)
        image_B = Image.fromarray(self.im_array_B)

        self.pixmapA_label.setPixmap(image_A.resize((400, 600)).toqpixmap())
        self.pixmapB_label.setPixmap(image_B.resize((400, 600)).toqpixmap())

        if self.active == self.imA:
            self.cur_im_arr = self.im_array_A
        elif self.active == self.imB:
            self.cur_im_arr = self.im_array_B

        self.radio_A.click()
        self.create_histogram()

    def save_image_A(self, fname):
        save_image(fname, self.im_array_A)

    def save_image_B(self, fname):
        save_image(fname, self.im_array_B)

    def save_image_AB(self, fname):
        im_array = np.concatenate((self.im_array_A, self.im_array_B), axis=1)
        save_image(fname, im_array)

    @Slot()
    def set_active_A(self):
        print("A")
        self.active = self.imA
        self.cur_im_arr = self.im_array_A
        self.create_histogram()

    @Slot()
    def set_active_B(self):
        self.active = self.imB
        self.cur_im_arr = self.im_array_B
        self.create_histogram()
        print("B")

    @Slot()
    def gaussian_blur(self):
        value = self.gauss_slider.value() / 2.5
        if self.active == self.imA:
            self.cur_im_arr = gaussian_blur(self.im_array_A, value)
        if self.active == self.imB:
            self.cur_im_arr = gaussian_blur(self.im_array_B, value)

        self.refresh_pixmap(self.cur_im_arr)
        self.gauss_label.setText(f"Gaussian blur: {value}")

    @Slot()
    def gamma_correction(self):
        value = self.gamma_slider.value() / 5
        if self.active == self.imA:
            self.cur_im_arr = gamma_correction(self.im_array_A, value)
        if self.active == self.imB:
            self.cur_im_arr = gamma_correction(self.im_array_B, value)

        self.refresh_pixmap(self.cur_im_arr)
        self.gamma_label.setText(f"Gamma correction: {value}")

    @Slot()
    def equalize_histogram(self):
        if self.active == self.imA:
            self.cur_im_arr = equalize_histogram(self.im_array_A)
        if self.active == self.imB:
            self.cur_im_arr = equalize_histogram(self.im_array_B)

        self.refresh_pixmap(self.cur_im_arr)
        self.apply_changes()

    @Slot()
    def median_filter(self):
        if self.active == self.imA:
            self.cur_im_arr = median_filter(self.im_array_A)
        if self.active == self.imB:
            self.cur_im_arr = median_filter(self.im_array_B)

        self.refresh_pixmap(self.cur_im_arr)
        self.apply_changes()

    @Slot()
    def sharpen(self):
        if self.active == self.imA:
            self.cur_im_arr = sharpen_mask(self.im_array_A)
        if self.active == self.imB:
            self.cur_im_arr = sharpen_mask(self.im_array_B)
        self.refresh_pixmap(self.cur_im_arr)
        self.apply_changes()

    @Slot()
    def apply_changes(self):
        if self.active == self.imA:
            self.history_A.append(self.im_array_A)
            self.im_array_A = self.cur_im_arr
        if self.active == self.imB:
            self.history_B.append(self.im_array_B)
            self.im_array_B = self.cur_im_arr
        self.create_histogram()

        self.gamma_slider.setValue(5)
        self.gauss_slider.setValue(0)

    @Slot()
    def undo(self):
        if self.active == self.imA:
            if len(self.history_A) == 0: return
            self.im_array_A = self.history_A.pop()
            self.refresh_pixmap(self.im_array_A)
        if self.active == self.imB:
            if len(self.history_B) == 0: return
            self.im_array_B = self.history_B.pop()
            self.refresh_pixmap(self.im_array_B)

        self.create_histogram()

    def refresh_pixmap(self, im_arr):
        image = Image.fromarray(im_arr)
        if self.active == self.imA:
            self.pixmapA_label.setPixmap(image.resize((400, 600)).toqpixmap())
        if self.active == self.imB:
            self.pixmapB_label.setPixmap(image.resize((400, 600)).toqpixmap())

    def create_histogram(self):
        histogram = compute_histogram(self.cur_im_arr)
        self._static_ax.clear()
        bins = histogram[1]
        vals = histogram[0]  # / np.sum(histogram[0])
        self._static_ax.bar(bins, vals)
        self._static_ax.set_yticklabels([])
        self._static_ax.figure.canvas.draw()
