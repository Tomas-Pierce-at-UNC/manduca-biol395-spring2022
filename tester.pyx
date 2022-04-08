
import glob
import random
import cine
import numpy as np
import skimage as sk
from matplotlib import pyplot

FILENAMES = glob.glob("../CineFilesOriginal/*.cine")
FILES = [cine.Cine(filename) for filename in FILENAMES]
# MEDIANS = [video.get_video_median() for video in FILES]

def get_random_image(video: cine.Cine) -> np.ndarray:
    index = random.randint(0, video.image_count - 1)
    image = video.get_ith_image(index)
    return image

def test(operation, *args, **kwargs):
    vid1 = random.choice(FILES)
    vid2 = random.choice(FILES)
    vid3 = random.choice(FILES)
    image1 = get_random_image(vid1)
    image2 = get_random_image(vid2)
    image3 = get_random_image(vid3)
    
    op1 = operation(image1, *args, **kwargs)
    op2 = operation(image2, *args, **kwargs)
    op3 = operation(image3, *args, **kwargs)

    fig,axes = pyplot.subplots(nrows=2, ncols=3)
    
    axes[0,0].imshow(image1)
    axes[1,0].imshow(op1)

    axes[0,1].imshow(image2)
    axes[1,1].imshow(op2)

    axes[0,2].imshow(image3)
    axes[1,2].imshow(op3)

    pyplot.show()
    
    return None

