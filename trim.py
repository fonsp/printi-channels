import os
import skimage.io
import numpy as np


def trim_file(path):
    original = skimage.io.imread(path)
    trimmed = trim(original)
    if trimmed is None:
        return 'all white'
    skimage.io.imsave(path, trimmed)


def trim(image):
    white_mask = np.equal(image, [255, 255, 255, 255])
    white_pixels = np.logical_and.reduce(white_mask, -1)
    white_rows = np.logical_and.reduce(white_pixels, -1)
    nonwhite_indices = np.logical_not(white_rows).nonzero()[0]
    if len(nonwhite_indices) == 0:
        return None
    last_included = nonwhite_indices[-1]
    return image[: last_included + 1, :, :]

