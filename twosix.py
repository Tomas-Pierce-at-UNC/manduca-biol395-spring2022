# test against moth 26, which fails in main.main()

import proboscis
import meniscus

import cine

from matplotlib import pyplot

import skimage as sk

if __name__ == '__main__':
    FILENAME = "../CineFilesOriginal/moth26_2022-02-15_freeflight.cine"

    c = cine.Cine(FILENAME)

    med1 = c.get_video_median()

    med2 = c.get_video_median()

    med3 = c.get_video_median()

    sk.io.imshow(med1)

    pyplot.show()

    sk.io.imshow(med2)

    pyplot.show()

    sk.io.imshow(med3)

    pyplot.show()
    
##    menx, meny = meniscus.get_meniscus(FILENAME)
##    px, py = proboscis.get_proboscis(FILENAME)
##
##    pyplot.scatter(menx, meny)
##    pyplot.show()
##
##    pyplot.scatter(px, py)
##    pyplot.show()
