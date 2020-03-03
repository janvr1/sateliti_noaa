from PIL import Image
import numpy as np
from skimage import filters as skfilt
from skimage import exposure as skexp
from skimage import img_as_ubyte


def load_image(fname):
    return Image.open(fname).convert('L')


def save_image(fname, im_arr):
    Image.fromarray(im_arr).save(fname, "png")


def gaussian_blur(im_arr, sigma):
    new_arr = skfilt.gaussian(im_arr, sigma)
    im = img_as_ubyte(np.clip(new_arr, -1, 1))
    return im


def gamma_correction(im_arr, gamma):
    return img_as_ubyte(skexp.adjust_gamma(im_arr, gamma))


def equalize_histogram(im_arr):
    return img_as_ubyte(skexp.equalize_hist(im_arr))


def compute_histogram(im_arr):
    return skexp.histogram(im_arr)
