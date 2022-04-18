import meniscus
import proboscis
from matplotlib import pyplot

FILENAME = "../CineFilesOriginal/deadMothTest_2022-01-28_Cine1.cine"

menx, meny = meniscus.get_meniscus(FILENAME)
px, py = proboscis.get_proboscis(FILENAME)

pyplot.scatter(menx, meny, marker='.', color='red')
pyplot.scatter(px, py, marker='.', color='blue')

pyplot.show()
