
EXNAME = "/home/tomas/Projects/BIOL395/CineFilesOriginal/moth23_2022-02-09_meh.cine"
START = -3834 + 5892
END = -1388 + 5892

EX2 = "/home/tomas/Projects/BIOL395/CineFilesOriginal/moth22_2022-02-07_Cine1.cine"

import numpy as np
import scipy
import skimage

import cine


def find_stand(image :np.ndarray):
    low = image - image.mean()
    gaussed = skimage.filters.gaussian(low)
    frame = np.zeros(image.shape, dtype=np.int32)
    for i in range(gaussed.shape[1]):
        col = gaussed[:,i]
        if all((val < 0 for val in col)):
            frame[:,i] = 1

    tubular = frame.astype(bool)
    return tubular
    if tubular.sum() == 0:
        return None
    left = None
    right = None
    
    for i in range(tubular.shape[1]):
        col = tubular[:,i]
        if all(col):
            left = i
            break
    for j in reversed(range(tubular.shape[1])):
        col = tubular[:,j]
        if all(col):
            right = j
            break

    return (left, right)

if __name__ == '__main__':
    video = cine.Cine(EXNAME)
    video2 = cine.Cine(EX2)

    median = video.get_video_median()
    m2 = video2.get_video_median()

    #video.close()
    #video2.close()

    bounds = find_stand(median)
    bounds2 = find_stand(m2)

    print(bounds)
    print(bounds2)
