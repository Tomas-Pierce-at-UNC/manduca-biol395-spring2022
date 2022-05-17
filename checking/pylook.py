
import array
import numpy
import skimage
from matplotlib import pyplot

with open("thing", "rb") as h:
    bits = h.read()

b = array.array("B", bits)
arr1 = numpy.array(b)
arr2 = numpy.reshape(arr1, (600, 800))
arr3 = numpy.flip(arr2, 0)
skimage.io.imshow(arr3)
pyplot.show()
