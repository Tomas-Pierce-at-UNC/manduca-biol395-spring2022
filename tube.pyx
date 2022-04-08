
import numpy as np
from skimage import filters, morphology as morpho


def split_zones(image: np.ndarray):
    return [image[:, i:i+100] for i in range(0, image.shape[1], 100)]


def get_low_li(image: np.ndarray):
    li = filters.threshold_li(image)
    return image < li


def get_col_region(image: np.ndarray, colbounds: tuple) -> np.ndarray:
    left, right = colbounds
    sub = image[:, left:right]
    return sub


def select_zones_1(image: np.ndarray):
    m1 = get_low_li(image)
    boundaries = [(i, i+100) for i in range(0, image.shape[1], 100)]
    mzones = split_zones(m1)
    totals = [mz.sum(0) for mz in mzones]
    vspans = [image.shape[0] in tot for tot in totals]
    pos_zones = [
        boundaries[i] for i in range(len(boundaries)) if not vspans[i]
        ]
    return pos_zones


def select_zones_2(image: np.ndarray):
    pos_zones = select_zones_1(image)
    edges = filters.roberts(image)
    iso = filters.threshold_isodata(edges)
    high = edges > iso
    counts = []
    for boundpair in pos_zones:
        region = get_col_region(high, boundpair)
        pcount = region.sum()
        counts.append(pcount)
    which = counts.index(max(counts))
    left, right = pos_zones[which]
    return (left - 25, right + 25)


def get_tallness_histogram(image: np.ndarray):
    verticals = filters.sobel_v(image)
    mags = np.abs(verticals)
    threshold = filters.threshold_isodata(mags)
    mask = mags > threshold
    skel = morpho.skeletonize(mask)
    heights = skel.sum(axis=0)
    colheights = [(i, height) for i, height in enumerate(heights)]
    return np.array(colheights)


def restricted_histogram(image: np.ndarray):
    left, right = select_zones_2(image)
    tallness = get_tallness_histogram(image)
    restricted = tallness[left:right]
    return restricted


def get_bounds_from_histogram(histogram: np.ndarray):
    avg = histogram.mean(0)[1]
    for lcol, count in histogram:
        if count > avg:
            break
    for rcol, count in reversed(histogram):
        if count > avg:
            break
    return (lcol, rcol)


def get_bounds(image: np.ndarray):
    reshist = restricted_histogram(image)
    left, right = get_bounds_from_histogram(reshist)
    return left - 5, right + 5


def restrict_to_bounds(image: np.ndarray, bounds: tuple):
    left, right = bounds
    return image[:, left:right]
