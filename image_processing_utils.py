import numpy as np
from skimage import segmentation, morphology, measure, color, feature, filters
from skimage import img_as_float
from scipy import ndimage
from sklearn.ensemble import RandomForestClassifier


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
    if img.ndim > 2:
        img = color.rgb2gray(img)
    labels = measure.label(mask)
    gradient_img = - ndimage.gaussian_gradient_magnitude(img, sigma)
    output = segmentation.watershed(gradient_img, labels)
    return output


def random_walker_segmentation(img, mask, beta=5000):
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
    if img.ndim > 2:
        img = color.rgb2gray(img)
    labels = measure.label(mask)
    output = segmentation.random_walker(img, labels, beta=beta, mode='cg_mg')
    return output


def _compute_features_gabor(im):
    gabor_frequencies = np.logspace(-5, 0.5, num=6, base=2)
    thetas = [0, np.pi/4., np.pi/2]
    nb_fq = len(gabor_frequencies) * len(thetas)
    im = np.atleast_3d(im)
    im_gabor = np.empty((im.shape[-1], nb_fq) + im.shape[:2])
    for ch in range(im.shape[-1]):
        img = img_as_float(im[..., ch])
        for i_fq, fq in enumerate(gabor_frequencies):
            for i_th, theta in enumerate(thetas):
                tmp = filters.gabor(img, fq, theta=theta)
                im_gabor[ch, len(thetas) * i_fq + i_th] = \
                                    np.abs(tmp[0] + 1j * tmp[1])
    return im_gabor


def random_forest_segmentation(img, mask, mode='gabor'):
    labels = measure.label(mask)
    if mode=='daisy':
        if img.ndim > 2:
            img = color.rgb2gray(img)
        radius = 15
        features = feature.daisy(img, step=1, radius=radius, rings=2,
                                            histograms=4)
        crop_labels = labels[radius:-radius, radius:-radius]
    elif mode=='gabor':
        features = _compute_features_gabor(img)
        nb_ch, nb_fq, sh_1, sh_2 = features.shape
        features = features.reshape((nb_ch * nb_fq, sh_1, sh_2))
        features = np.moveaxis(features, 0, -1)
        crop_labels = labels
    X_train = features[crop_labels >0, :]
    Y_train=crop_labels[crop_labels>0]
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(X_train, Y_train)
    output = rf.predict(features.reshape(-1, features.shape[2]))
    output = output.reshape(crop_labels.shape)
    output[crop_labels>0] = crop_labels[crop_labels>0]
    return output


def segmentation_generic(img, mask, mode='watershed'):
    if mode=='watershed':
        return watershed_segmentation(img, mask)
    elif mode=='random_walker':
        return random_walker_segmentation(img, mask)
    elif mode=='random_forest':
        return random_forest_segmentation(img, mask)
    else:
        raise NotImplementedError
