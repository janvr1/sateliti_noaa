import numpy as np
from PIL import Image
from skimage import exposure as skexp
from skimage import filters as skfilt
from skimage import img_as_ubyte
from skimage import restoration as skrestore

from numba import jit, njit

import time as time


def load_image(fname):
    return split_image(np.array(Image.open(fname).convert('L')))


def split_image(im_arr):
    imA = np.array(im_arr[:, :1040])
    imB = np.array(im_arr[:, 1040:])
    return imA, imB


def save_image(fname, im_arr):
    Image.fromarray(im_arr).save(fname, format="png")


@jit(forceobj=True)
def gaussian_blur(im_arr, sigma):
    start = time.time()
    new_arr = skfilt.gaussian(im_arr, sigma)
    im = img_as_ubyte(np.clip(new_arr, -1, 1))
    print(time.time() - start)
    return im


@jit(forceobj=True)
def gamma_correction(im_arr, gamma):
    return img_as_ubyte(skexp.adjust_gamma(im_arr, gamma))


def equalize_histogram(im_arr):
    return img_as_ubyte(skexp.equalize_hist(im_arr))


def compute_histogram(im_arr):
    return skexp.histogram(im_arr)


def median_filter(im_arr):
    return img_as_ubyte(skfilt.median(im_arr))


def denoise_wavelet(im_arr):
    return img_as_ubyte(skrestore.denoise_wavelet(im_arr, 2))


def denoise_bilateral(im_arr):
    return img_as_ubyte(skrestore.denoise_bilateral(im_arr))


def sharpen_mask(im_arr):
    return img_as_ubyte(skfilt.unsharp_mask(im_arr))


def false_color(im_arr_A, im_arr_B):
    kA = 0.8
    kB = 1 - kA
    mid_im = kA * im_arr_A + kB * im_arr_B
    mid_im = np.round(mid_im).astype('uint8')

    color_im = np.dstack([mid_im, im_arr_A, im_arr_B])

    return color_im
