import numpy as np
from skimage import io, measure, feature


def register_tiles(imgs, n_rows, n_cols, overlaps=None, pad=None):
    if pad is None:
        pad = 200
    l_r, l_c = imgs.shape[2:4]
    if overlaps is None:
        overlaps = 0.25
    if np.isscalar(overlaps):
        overlaps = np.array([float(overlaps), ] * (n_rows * n_cols - 1))
    overlap = (l_r * np.array(overlaps)).astype(np.int)
    if imgs.ndim == 4:
        canvas = np.zeros((2 * pad + n_rows * l_r, 2 * pad + n_cols * l_c),
                      dtype=imgs.dtype)
    else:
        canvas = np.zeros((2 * pad + n_rows * l_r, 2 * pad + n_cols * l_c, 3),
                      dtype=imgs.dtype)
    init_r, init_c = pad, pad
    canvas[init_r:init_r + l_r, init_c:init_c + l_c] = imgs[0, 0]
    shifts = np.empty((n_rows, n_cols, 2), dtype=np.int)
    shifts[0, 0] = init_r, init_c
    counter = 0
    for i_rows in range(n_rows):
        if i_rows >= 1:
            init_r, init_c = shifts[i_rows - 1, 0]
            init_r += l_r
            shift_vert = feature.register_translation(
                    imgs[i_rows - 1, 0, -overlap[counter]:],
                    imgs[i_rows, 0, :overlap[counter]])[0]
            init_r += int(shift_vert[0])  - overlap[counter]
            init_c += int(shift_vert[1])
            shifts[i_rows, 0] = init_r, init_c
            canvas[init_r:init_r + l_r, init_c:init_c + l_c] = imgs[i_rows,
                                                                    0]
            counter += 1
        for j_cols in range(n_cols - 1):
            init_c += l_c
            shift_horiz = feature.register_translation(
                imgs[i_rows, j_cols, :, -overlap[counter]:], 
                imgs[i_rows, j_cols+1, :, :overlap[counter]])[0]
            print("shift", shift_horiz)
            init_r += int(shift_horiz[0])
            init_c += int(shift_horiz[1]) - overlap[counter]
            shifts[i_rows, j_cols + 1] = init_r, init_c
            counter += 1
            canvas[init_r:init_r + l_r, init_c:init_c + l_c] = imgs[i_rows,
                                                                    j_cols+1]
    return canvas
