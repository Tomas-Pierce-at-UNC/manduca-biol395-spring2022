
FILENAME = "./bytes"

with open(FILENAME, "rb") as handle:
	bits = handle.read()

import numpy as np
import array

arr = array.array("B", bits)

nar = np.array(arr)

res = np.reshape(nar, (600,800))

res = np.flip(res, 0)

import skimage
from matplotlib import pyplot

skimage.io.imshow(res)
pyplot.show()