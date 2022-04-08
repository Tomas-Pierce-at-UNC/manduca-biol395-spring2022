# restrict the rows which are actually required

import numpy as np
from skimage import filters
import cine


def get_edges(image: np.ndarray) -> np.ndarray:
    h = filters.sobel_h(image)
    h[h > 0] = 0
    return h


def get_widths(edges: np.ndarray) -> np.ndarray:
    wides = edges.sum(1)
    wide_mags = np.abs(wides)
    return wide_mags

def get_bottom(widths: np.ndarray) -> int:
    ws = list(widths)
    where = ws.index(max(ws))
    return where

def get_top(widths: np.ndarray, bottom: int) -> int:
    zone = widths[:bottom]
    half = len(zone) // 2
    zone = zone[:half]
    gradient = np.gradient(zone)
    grads = list(gradient)
    where = grads.index(max(grads))
    return where

def get_bounds(image: np.ndarray) -> tuple:
    edges = get_edges(image)
    widths = get_widths(edges)
    bottom = get_bottom(widths)
    top = get_top(widths, bottom)
    return top, bottom

def restrict(image: np.ndarray, bounds: tuple) -> np.ndarray:
    top, bottom = bounds
    return image[top:bottom]

# TODO: use total / range measurement to choose top and bottom rows

# TODO: restrict image to area between top and bottom rows

if __name__ == '__main__':

    from skimage import io as skio
    from matplotlib import pyplot
    
    c = cine.Cine("../CineFilesOriginal/moth22_2022-02-04_Cine1.cine")
    f20 = c.get_ith_image(20)
    median1 = c.get_video_median()
    c.close()
    bounds1 = get_bounds(median1)
    resmedian1 = restrict(median1, bounds1)
    

    c2 = cine.Cine("../CineFilesOriginal/moth26_2022-02-15_freeflight.cine")
    median2 = c2.get_video_median()
    c2.close()
    bounds2 = get_bounds(median2)
    resmedian2 = restrict(median2, bounds2)
    
    skio.imshow(resmedian1)
    pyplot.show()
    skio.imshow(resmedian2)
    pyplot.show()
