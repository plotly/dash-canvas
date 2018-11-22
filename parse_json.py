import numpy as np
import json
from skimage import draw, morphology
from scipy import ndimage


def _indices_of_path(path):
    rr, cc = [], []
    for (Q1, Q2) in zip(path[:-2], path[1:-1]):
        inds = draw.bezier_curve(int(Q1[-1]), int(Q1[-2]), 
                                 int(Q2[2]), int(Q2[1]), 
                                 int(Q2[4]), int(Q2[3]), 1)
        rr += list(inds[0])
        cc += list(inds[1])
    return rr, cc


def parse_jsonstring(string, shape=None):
    """
    Parse JSON string to draw the path saved by react-sketch.

    Parameters
    ----------

    data : str
        JSON string of data
    shape: tuple, optional
        shape of returned image.
    """
    if shape is None:
        shape = (500, 500)
    mask = np.zeros(shape, dtype=np.bool)
    try:
        data = json.loads(string)
    except TypeError:
        return mask

    for obj in data['objects']:
        if obj['type'] == 'path':
            inds = _indices_of_path(obj['path'])
            radius = obj['strokeWidth'] // 2
            mask_tmp = np.zeros(shape, dtype=np.bool)
            mask_tmp[inds[0], inds[1]] = 1
            mask_tmp = ndimage.binary_dilation(mask_tmp,
                                                  morphology.disk(radius))
            mask += mask_tmp
    return mask


def parse_jsonfile(filename, shape=None):
    with open(filename, 'r') as fp:
        string = json.load(fp)
    return parse_jsonstring(string, shape=shape)


