"""Functions to process images with Gabor filters"""


import os
from multiprocessing import Pool
import numpy as np
from matplotlib import pyplot as plt
from skimage.filters import gabor_kernel
from skimage.io import imread, imsave, imshow
from skimage.viewer import ImageViewer
from skimage.transform import resize, rescale
from scipy.signal import convolve2d
from scipy.ndimage.filters import gaussian_filter
import video_processing


def _get_filters():
    filters = []
    angles = np.linspace(.25, .35, 5)
    filters.extend([gabor_kernel(0.2, theta=np.pi * alpha, sigma_x=2, sigma_y=6)
                    for alpha in angles])
    filters.extend([gabor_kernel(0.2, theta=np.pi * alpha, sigma_x=3, sigma_y=9)
                    for alpha in angles])
    return filters


def get_best_filter(rescaling_factor):
    scale = (_get_video_width() / 1280) * (rescaling_factor / .4)
    pixel_frequency = .2 / scale
    theta = .3 * np.pi
    sigma_x = 2 * scale
    sigma_y = 3 * scale
    kernel_for_left_lane = gabor_kernel(pixel_frequency,
                                        theta=theta,
                                        sigma_x=sigma_x,
                                        sigma_y=sigma_y)
    kernel_for_right_lane = gabor_kernel(pixel_frequency,
                                         theta=-theta,
                                         sigma_x=sigma_x,
                                         sigma_y=sigma_y)
    return .5 * (kernel_for_left_lane + kernel_for_right_lane)


def _get_video_width():
    first_frame = load_frame(frame_number=0, rescaling_factor=1)
    return first_frame.shape[1]


def load_frame(frame_number, rescaling_factor):
    path = os.path.join('frames', 'frame{0}.png'.format(str(frame_number).zfill(5)))
    return rescale(imread(path, as_grey=True), rescaling_factor)


def show(image):
    ImageViewer(image).show()


def show_tiled(images):
    n_per_side = int(np.sqrt(len(images)) + 1)
    plt.figure(figsize=(3*n_per_side, 3*n_per_side))
    for i, g in enumerate(images):
        plt.gcf().add_subplot(n_per_side, n_per_side, i+1)
        plt.imshow(g.real, cmap='gray')
    plt.show()


def _convolve(filter_grayscale_pair):
    f, grayscale = filter_grayscale_pair
    return convolve2d(f.real, grayscale)


def apply_filters(filters, grayscale, num_processes):
    """Convolve each filter in a collection of filters with a single image"""
    pool = Pool(num_processes)
    return pool.map(_convolve, ((f, grayscale) for f in filters))


def apply_filter(f, grayscales, num_processes):
    """Convolve a filter with each image in a collection"""
    pool = Pool(num_processes)
    return pool.map(_convolve, ((f, grayscale) for grayscale in grayscales))


def get_activations(convolved, quantile):
    """Finds the pixels at which the convolution exceeds a threshold"""
    return convolved > np.percentile(convolved, quantile * 100)


def save_activations(activations, directory):
    for i, activation in enumerate(activations):
        imsave(os.path.join(directory, 'frame{0}.png'.format(str(i).zfill(5))), activation * 255)
