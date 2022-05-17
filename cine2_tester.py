import cine2

import glob

import skimage
from matplotlib import pyplot

files = glob.glob("/home/tomas/Projects/BIOL395/CineFilesOriginal/*.cine")

vid1 = cine2.Cine(files[0])
vid2 = cine2.Cine(files[1])

med1 = vid1.get_video_median()
med2 = vid2.get_video_median()

skimage.io.imshow(med1)
pyplot.show()

skimage.io.imshow(med2)
pyplot.show()

vid1.close()
vid2.close()

#for filename in files:

#	cine = cine2.Cine(filename)

#	med1 = cine.get_video_median()
#	med2 = cine.get_video_median()
#
#	skimage.io.imshow(med1)
#	pyplot.show()

#	skimage.io.imshow(med2)
#	pyplot.show()

#	cine.close()

