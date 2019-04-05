import plotly.graph_objs as go
import PIL
import numpy as np
from skimage import color, img_as_ubyte


def image_with_contour(img, labels, shape=None):
    """
    Figure with contour plot of labels superimposed on background image.

    Parameters
    ----------

    img : URL, dataURI or ndarray
        Background image. If a numpy array, it is transformed into a PIL
        Image object.
    labels : 2D ndarray
        Contours are the isolines of labels.
    shape: tuple, optional
        Shape of the arrays, to be provided if ``img`` is not a numpy array.
    """
    try:
        sh_y, sh_x = shape if shape is not None else img.shape
    except AttributeError:
        print('''the shape of the image must be provided with the
                 ``shape`` parameter if ``img`` is not a numpy array''')
    if type(img) == np.ndarray:
        img = img_as_ubyte(color.gray2rgb(img))
        img = PIL.Image.fromarray(img)
    labels = labels.astype(np.float)
    # Contour plot of segmentation
    cont = go.Contour(z=labels[::-1],
            contours=dict(coloring='lines'),
            line=dict(width=3),
            showscale=False,
            )
    # Layout
    layout= go.Layout(
            images = [dict(
                  source=img,
                  xref="x",
                  yref="y",
                  x=0,
                  y=sh_y,
                  sizex=sh_x,
                  sizey=sh_y,
                  sizing="contain",
                  layer="below")],
            xaxis=dict(
                  showgrid=False,
                  zeroline=False,
                  showline=False,
                  ticks='',
                  showticklabels=False,
                  ),
            yaxis=dict(
                  showgrid=False,
                  zeroline=False,
                  showline=False,
                  scaleanchor="x",
                  ticks='',
                  showticklabels=False,
    ))
    fig = go.Figure(data=[cont], layout=layout)
    return fig


if __name__ == '__main__':
    from skimage import data
    import plotly.plotly as py
    camera = data.camera()
    fig = image_with_contour(camera, camera > 150)
    py.iplot(fig)
