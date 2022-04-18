# try and test multiple video feedings for completeness

import proboscis
import meniscus

import glob

from matplotlib import pyplot

filename = "../CineFilesOriginal/moth22_2022-02-04_Cine1.cine"
start_index = -1642 + 1800
end_index = -1332 + 1800


xmen, men = meniscus.get_meniscus(filename, start_index, end_index)
xp, probs = proboscis.get_proboscis(filename, start_index, end_index)

