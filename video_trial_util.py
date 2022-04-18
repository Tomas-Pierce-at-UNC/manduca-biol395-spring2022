# try each video to check behavior

import meniscus
import proboscis

vid1 = "../CineFilesOriginal/moth22_2022-01-26.cine"

mx, md = meniscus.get_meniscus(vid1)
px, pd = proboscis.get_proboscis(vid1)

