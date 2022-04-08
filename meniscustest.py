
import meniscus
import numpy as np
from matplotlib import pyplot

if __name__ == '__main__':

    filename1 = "../CineFilesOriginal/moth23_2022-02-09_meh.cine"
    mens1 = []
    video_meniscus_rows = meniscus.measure_meniscus_in_video(
        filename1,
        start=2131,
        end=4619
        )
    for row_coord in video_meniscus_rows:
        print(row_coord)
        mens1.append(row_coord)
    mens1 = np.array(mens1)

    pyplot.plot(mens1)
    pyplot.show()
