import numpy as np
from skimage import segmentation, morphology, measure
from scipy import ndimage

def watershed_segmentation(img, mask, sigma=4):
    labels = measure.label(mask)
    gradient_img = - ndimage.gaussian_gradient_magnitude(img, sigma)
    output = segmentation.watershed(gradient_img, labels)
    return output
