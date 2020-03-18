import numpy as np
from PIL import Image
from skimage import exposure as skexp
from skimage import filters as skfilt
from skimage import img_as_ubyte
from skimage import restoration as skrestore


def load_image(fname):
    return split_image(np.array(Image.open(fname).convert('L')))


def split_image(im_arr):
    imA = np.array(im_arr[:, :1040])
    imB = np.array(im_arr[:, 1040:])
    return imA, imB


def save_image(fname, im_arr):
    Image.fromarray(im_arr).save(fname)


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


def median_filter(im_arr):
    return img_as_ubyte(skfilt.median(im_arr))


def denoise_wavelet(im_arr):
    return img_as_ubyte(np.clip(skrestore.denoise_nl_means(im_arr), -1, 1))


def denoise_bilateral(im_arr):
    return img_as_ubyte(skrestore.denoise_bilateral(im_arr))


def denoise_tv(im_arr):
    return img_as_ubyte(skrestore.denoise_tv_chambolle(im_arr, weight=0.1))


def find_edges_scharr(im_arr):
    return img_as_ubyte(skfilt.scharr(im_arr))


def sharpen_mask(im_arr):
    return img_as_ubyte(skfilt.unsharp_mask(im_arr))


def false_color(im_arr_A, im_arr_B):
    A = im_arr_A
    B = im_arr_B

    # old method
    # kA = 0.9
    # kB = 1 - kA
    # C = kA * im_arr_A + kB * im_arr_B
    # C = np.round(C).astype('uint8')

    s = 180
    k = -np.log(0.2) * 2 / s
    C = A.copy().astype('float64')
    K = np.exp(k * (C - s))[np.where(A < s)]
    C[np.where(A < s)] = K * A[np.where(A < s)]
    C = np.round(C).astype('uint8')

    color_im = np.dstack([C, A, B])

    return color_im
