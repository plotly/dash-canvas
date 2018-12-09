from image_processing_utils import watershed_segmentation
from skimage import data
import numpy as np


def test_watershed_segmentation():
    img = np.zeros((20, 20))
    img[2:6, 2:6] = 1
    img[10:15, 10:15] = 1
    mask = np.zeros_like(img, dtype=np.uint8)
    mask[4, 4] = 1
    mask[12, 12] = 2
    res = watershed_segmentation(img, mask, sigma=0.1)
    assert np.all(res[2:6, 2:6] == 1)
    assert np.all(res[10:15, 10:15] == 2)

