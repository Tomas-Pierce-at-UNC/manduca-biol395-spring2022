
import numpy as np
import align


def subtract(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return left.astype(np.int16) - right.astype(np.int16)


def setup(image: np.ndarray, bg: np.ndarray, al: align.Aligner) -> np.ndarray:
    lined = al.align(image)
    delta = subtract(lined, bg)
    return delta

