# test against moth 26, which fails in main.main()

import proboscis
import meniscus

FILENAME = "../CineFilesOriginal/moth26_2022-02-15_freeflight.cine"

menx, meny = meniscus.get_meniscus(FILENAME)
px, py = proboscis.get_proboscis(FILENAME)
