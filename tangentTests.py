# for stuff that is more exploratory than directly related to the goal

import meniscus
import proboscis
from matplotlib import pyplot

FILENAME = "../CineFilesOriginal/moth22_2022-02-01b_Cine1.cine"

x_es, mens = meniscus.get_meniscus(FILENAME)
xxes, ps = proboscis.get_proboscis(FILENAME)

pyplot.scatter(x_es, mens)
pyplot.show()

pyplot.scatter(xxes, ps)
pyplot.show()
