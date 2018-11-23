import numpy as np
from skimage import segmentation, morphology, measure
from scipy import ndimage


def watershed_segmentation(img, mask, sigma=4):
    """
    Watershed segmentation of image using annotations as label markers.

    The image used for the watershed is minus the gradient of the original
    image, convoluted with a Gaussian for more robustness.

    Parameters
    ----------

    img : ndarray
        image to be segmented
    mask : ndarray of ints
        binary array, each connected component corresponds to a different
        object to be segmented
    sigma : float
        standard deviation of Gaussian convoluting the gradient. Increase
        for smoother boundaries.
    """
    labels = measure.label(mask)
    gradient_img = - ndimage.gaussian_gradient_magnitude(img, sigma)
    output = segmentation.watershed(gradient_img, labels)
    return output
