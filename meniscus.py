
import cine
import align
import tube
import row
from skimage import filters
from skimage import io as skio
from skimage import morphology as morpho
from skimage import exposure
from skimage import feature
from skimage import measure
from matplotlib import pyplot
import numpy as np
import math


def isolate(filename: str, start=0, end=None):
    try:
        video = cine.Cine(filename)
        median = video.get_video_median()
        bounds = tube.get_bounds(median)
        row_bounds = row.get_bounds(median)
        print(bounds)
        aligner = align.Aligner(median)
        if end is None:
            end = video.image_count
        for i in range(start, end):
            frame = video.get_ith_image(i)
            try:
                aligned = aligner.align(frame)
            except ValueError as e:
                print(i)
                skio.imshow(frame)
                pyplot.show()
                breakpoint()
            delta = aligned.astype(np.int16) - median.astype(np.int16)
            restricted_delta = tube.restrict_to_bounds(delta, bounds)
            restricted_delta = row.restrict(restricted_delta, row_bounds)
            restricted_delta[restricted_delta > 0] = 0
            iso = filters.threshold_isodata(restricted_delta)
            low = restricted_delta < (iso * 1.5)
            yield low
    finally:
        video.close()


def get_canidates(mask: np.ndarray):
    blobs = feature.blob_log(mask)
    canidates = blobs[blobs[:,2] > 1]
    return canidates


def get_canidate_masks(canidates: np.ndarray, scene: np.ndarray) -> list:
    masks = []
    # want to remove holes so that a off pixel surrounded by on pixels
    # gets treated as being an actual point
    myscene = morpho.closing(scene)
    labels = measure.label(myscene)
    for canidate in canidates:
        row, col, sigma = canidate
        tag = labels[int(row),int(col)]
        if tag == 0:
            continue
        submask = labels == tag
        masks.append(submask)
    return masks

def get_width(region):
    major = region.axis_major_length
    orient = region.orientation
    return math.cos(orient) * major

def select(canidate_masks):
    if len(canidate_masks) == 1:
        return canidate_masks[0]
    else:
        widest = 0
        widemask = None
        for i,mask in enumerate(canidate_masks):
            regionprops = measure.regionprops(mask.astype(np.uint8))[0]
            width = get_width(regionprops)
            wideness = abs(width)
            if wideness > widest:
                widest = wideness
                widemask = mask
        return widemask

def find_meniscus_row(meniscus_mask):
    img = meniscus_mask.astype(np.uint8)
    props = measure.regionprops(img)[0]
    centroid = props.centroid
    return centroid[0]

def measure_meniscus_in_video(filename, start = 0, end = None):
    isolateds = isolate(filename, start, end)
    for mask in isolateds:
        canidates = get_canidates(mask)
        can_masks = get_canidate_masks(canidates, mask)
        meniscus_mask = select(can_masks)
        meniscus_row = find_meniscus_row(meniscus_mask)
        yield meniscus_row

if __name__ == '__main__':

    filename1 = "../CineFilesOriginal/moth23_2022-02-09_meh.cine"
    mens1 = []
    #video_meniscus_rows = measure_meniscus_in_video(filename1, start=2131, end=4619)
    video_meniscus_rows = measure_meniscus_in_video(filename1, start=2131, end=2431)
    for row_coord in video_meniscus_rows:
        print(row_coord)
        mens1.append(row_coord)
    mens1 = np.array(mens1)

    positions = np.arange(0, len(mens1))
    pyplot.scatter(positions, mens1, marker='.')
    pyplot.show()
    
##    filename2 = "../CineFilesOriginal/moth26_2022-02-15_freeflight.cine"
##    vid_men_rows = measure_meniscus_in_video(filename2, start=10)
##    mens2 = []
##    for row_coord in vid_men_rows:
##        print(row_coord)
##        mens2.append(row_coord)
##    mens2 = np.array(mens2)
##
##    filename3 = "../CineFilesOriginal/moth23_2022-02-09_meh.cine"
##    vmr = measure_meniscus_in_video(filename3, start=2061, end=4618)
##    mens3 = []
##    for row_coord in vmr:
##        print(row_coord)
##        mens3.append(row_coord)
##    mens3 = np.array(mens3)
    
    
##    filename = "../CineFilesOriginal/moth22_2022-02-04_Cine1.cine"
##    isol = isolate(filename, start=20)
##    begin = next(isol)
##    bcans = get_canidates(begin)
##    bcan_masks = get_canidate_masks(bcans, begin)
##    b_men_mask = select(bcan_masks)
##    bmen = find_meniscus_row(b_men_mask)
##    print("meniscus of b at", bmen)
##
##    fname = "../CineFilesOriginal/moth26_2022-02-15_freeflight.cine"
##    isol2 = isolate(fname, start=10)
##    initial = next(isol2)
##    icans = get_canidates(initial)
##    ican_masks = get_canidate_masks(icans, initial)
##    i_men_mask = select(ican_masks)
##    imen = find_meniscus_row(i_men_mask)
##    print("meniscus of i at", imen)
##
##    file = "../CineFilesOriginal/moth23_2022-02-09_meh.cine"
##    isol3 = isolate(file, 2061, 4618)
##    start = next(isol3)
##    scans = get_canidates(start)
##    scan_masks = get_canidate_masks(scans, start)
##    s_men_mask = select(scan_masks)
##    smen = find_meniscus_row(s_men_mask)
##    print("meniscus of s at", smen)
##
##    skio.imshow(begin)
##    pyplot.show()
##    skio.imshow(b_men_mask)
##    pyplot.show()
##
##    skio.imshow(initial)
##    pyplot.show()
##    skio.imshow(i_men_mask)
##    pyplot.show()
##
##    skio.imshow(start)
##    pyplot.show()
##    skio.imshow(s_men_mask)
##    pyplot.show()
