
import cine
import tube
import meniscus
import proboscis
import align
import skimage as sk
import numpy as np
from matplotlib import pyplot

FILENAME = "../CineFilesOriginal/moth22_2022-02-09_okay.cine"
vcine = cine.Cine(FILENAME)
m = vcine.get_video_median()
sk.io.imsave("/home/tomas/Documents/BIOL395/exVidMedian.png", m)
aligner = align.Aligner(m)
bounds = tube.get_bounds(m)
resm = tube.restrict_to_bounds(m, bounds)
sk.io.imsave("/home/tomas/Documents/BIOL395/exTubeRes.png", resm)
t2 = vcine.get_ith_image(2000)
delta = t2.astype(np.int16) - m.astype(np.int16)

delta = tube.restrict_to_bounds(delta, bounds)
sk.io.imsave("/home/tomas/Documents/BIOL395/exDelta.png", delta)

vcine.close()

menisol = meniscus.isolate(FILENAME, 2000, 2005)
menmask1 = next(menisol)
# resMen = tube.restrict_to_bounds(menmask1, bounds)
sk.io.imsave("/home/tomas/Documents/BIOL395/exMenMask.png", menmask1)

probosil = proboscis.isolate(FILENAME, 2000, 2005)
probmask1 = next(probosil)
# resProb = tube.restrict_to_bounds(probmask1, bounds)
sk.io.imsave("/home/tomas/Documents/BIOL395/exProbMask.png", probmask1)

