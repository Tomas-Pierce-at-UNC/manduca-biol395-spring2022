# test each video in the thing

import meniscus
import proboscis
import glob
from matplotlib import pyplot

VIDEOS = glob.glob("../CineFilesOriginal/*.cine")

for i, vidname in enumerate(VIDEOS):
    mx, md = meniscus.get_meniscus(vidname)
    px, pd = proboscis.get_proboscis(vidname)
    pyplot.scatter(mx, md, marker='.', color='red')
    pyplot.scatter(px, pd, marker='.', color='blue')
    pyplot.savefig("video{}.png".format(i))
