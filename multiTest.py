
# run multiple videos with meniscus and proboscis to at the same time test
# meniscus measurement and proboscis measurement

#import multiprocessing as multi
import threading
# note that this is actually slower than running them one at a time

import meniscus
import proboscis

from matplotlib import pyplot

keywords1 = {
    "filename": "../CineFilesOriginal/moth23_2022-02-09_meh.cine",
    "start": 2131,
    "end": 2431
}

keywords2 = {
    "filename": "../CineFilesOriginal/moth22_2022-02-04_Cine1.cine",
    "start": 189,
    "end": 590
}




def plot_meniscus(keywords):
    xs, mens = meniscus.get_meniscus(**keywords)
    pyplot.scatter(xs, mens)
    pyplot.title(keywords["filename"] + " meniscus")
    pyplot.show()


def plot_proboscis(keywords):
    xs, probs = proboscis.get_proboscis(**keywords)
    pyplot.scatter(xs, probs)
    pyplot.title(keywords["filename"] + " proboscis")
    pyplot.show()

if __name__ == '__main__':
    t1 = threading.Thread(target=plot_meniscus, args=(keywords1,))
    t2 = threading.Thread(target=plot_meniscus, args=(keywords2,))

    t3 = threading.Thread(target=plot_proboscis, args=(keywords1,))
    t4 = threading.Thread(target=plot_proboscis, args=(keywords1,))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    print("all started")
    t1.join()
    t2.join()
    t3.join()
    t4.join()
