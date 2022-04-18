
import cine
import align
import tube
# import row
import point
from matplotlib import pyplot
import numpy as np
from skimage import filters
from skimage import io as skio
from skimage import measure


def isolate(filename: str, start: int = 0, end: int = None):
    video = cine.Cine(filename)
    median = video.get_video_median()
    col_bounds = tube.get_bounds(median)
    # row_bounds = row.get_bounds(median)
    print(col_bounds) # , row_bounds)
    aligner = align.Aligner(median)
    if end is None:
        end = video.image_count
    for i in range(start, end):
        frame = video.get_ith_image(i)
        try:
            aligned = aligner.align(frame)
        except ValueError:
            print(i)
            skio.imshow(frame)
            pyplot.show()
            breakpoint()
        except AttributeError:
            print(filename)
            print("Unable to align frame {}".format(i))
            yield -1
            continue
        delta = aligned.astype(np.int16) - median.astype(np.int16)
        restricted_delta = tube.restrict_to_bounds(delta, col_bounds)
        # restricted_delta = row.restrict(restricted_delta, row_bounds)
        restricted_delta[restricted_delta > 0] = 0
        iso = filters.threshold_isodata(restricted_delta)
        low = restricted_delta < iso
        yield low
    video.close()


def get_zones(mask):
    labeled = measure.label(mask, connectivity=2)
    zone_names = np.unique(labeled)
    zone_names = zone_names[zone_names != 0]
    zones: dict = {}
    for name in zone_names:
        zones[name] = []

    for r, imrow in enumerate(labeled):
        for c, val in enumerate(imrow):
            if val == 0:
                continue
            p = point.Point(r, c)
            zones[val].append(p)
    return list(zones.values())


def lowest_of_zone(zone: list):
    return max(zone, key=lambda point: point.row)


def measure_proboscis_position(pos_zones: list):
    largest = list(filter(lambda z: len(z) >= 10, pos_zones))
    max_y_pt = max(
        map(
            lowest_of_zone, largest),
        key=lambda point: point.row
        )
    return max_y_pt.row


def measure_proboscis_in_video(filename, start: int = 0, end: int = None):
    isolated = isolate(filename, start, end)
    for mask in isolated:
        zones = get_zones(mask)
        pos = measure_proboscis_position(zones)
        yield pos


def get_proboscis(filename: str, start: int = 0, end: int = None):
    mmnts = measure_proboscis_in_video(filename, start, end)
    positions = []
    for row_coord in mmnts:
        print(row_coord)
        positions.append(row_coord)
    positions = np.array(positions)
    if end is None:
        xs = np.arange(0, len(positions))
    else:
        xs = np.arange(start, end)

    return xs, positions

if __name__ == '__main__':

##    #test 1
##    filename1 = "../CineFilesOriginal/moth23_2022-02-09_meh.cine"
##    mmnts = measure_proboscis_in_video(filename1, 2131, 2431)
##    positions = []
##    for row_coord in mmnts:
##        print(row_coord)
##        positions.append(row_coord)
##
##    positions = np.array(positions)
##    xs = np.arange(2131, 2431)
##
##    pyplot.scatter(xs, positions, marker='.')
##    pyplot.show()

    #test 2
    filename2 = "../CineFilesOriginal/moth22_2022-02-07_Cine1.cine"
    xs,positions = get_proboscis(filename2)
    pyplot.scatter(xs, positions, marker='.')
    pyplot.show()
    
