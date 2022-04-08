
import cine
import align
import tube
from skimage import filters
import numpy as np


def isolate(filename: str, start=0, end=None):
    video = cine.Cine(filename)
    median = video.get_video_median()
    bounds = tube.get_bounds(median)
    print(bounds)
    aligner = align.Aligner(median)
    if end is None:
        end = video.image_count
    for i in range(start, end):
        frame = video.get_ith_image(i)
        aligned = aligner.align(frame)
        delta = aligned.astype(np.int16) - median.astype(np.int16)
        restricted_delta = tube.restrict_to_bounds(delta, bounds)
        restricted_delta[restricted_delta > 0] = 0
        yield restricted_delta

def get_canidates(mask: np.ndarray):
    pass

def select(canidates):
    pass

def measure(tongue_place):
    pass

if __name__ == '__main__':
    filename = "../CineFilesOriginal/moth22_2022-02-04_Cine1.cine"
    isol = isolate(filename, start=20)
    begin = next(isol)

    fname = "../CineFilesOriginal/moth26_2022-02-15_freeflight.cine"
    isol2 = isolate(fname, start=10)
    initial = next(isol2)

    file = "../CineFilesOriginal/moth23_2022-02-09_meh.cine"
    isol3 = isolate(file, 2061, 4618)
    start = next(isol3)
