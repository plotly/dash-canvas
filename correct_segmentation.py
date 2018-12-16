import numpy as np
import json
from skimage import io, color, segmentation, img_as_ubyte, filters, measure
from PIL import Image


import dash_canvas
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from parse_json import parse_jsonstring
from io_utils import image_string_to_PILImage, array_to_data_url
from image_processing_utils import modify_segmentation

# Image to segment and shape parameters
filename = 'https://upload.wikimedia.org/wikipedia/commons/1/1b/HumanChromosomesChromomycinA3.jpg'
img = io.imread(filename, as_gray=True)
mask = img > 1.2 * filters.threshold_otsu(img)
labels = measure.label(mask)


overlay = segmentation.mark_boundaries(img, labels)
overlay = img_as_ubyte(overlay)

height, width = img.shape[:2]
canvas_width = 500
canvas_height = round(height * canvas_width / width)
scale = canvas_width / width
print(scale, canvas_height)

# ------------------ App definition ---------------------

app = dash.Dash(__name__)

server = app.server

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})



app.layout = html.Div([
    html.Div([
    html.H2(children='Manual correction of automatic segmentation'),
    dash_canvas.DashCanvas(
        id='canvas',
        label='my-label',
        width=canvas_width,
	height=canvas_height,
        scale=scale,
        lineWidth=2,
        lineColor='red',
        image_content=array_to_data_url(overlay),
    ),
     ], className="six columns"),
    ])

# ----------------------- Callbacks -----------------------------
@app.callback(Output('canvas', 'image_content'),
             [Input('canvas', 'trigger'),],
             [State('canvas', 'json_data'),
              State('canvas', 'scale'),
              State('canvas', 'height'),
	      State('canvas', 'width')])
def update_segmentation(toggle, string, s, h, w):
    mask = parse_jsonstring(string, shape=(height, width))
    new_labels = modify_segmentation(labels, mask, img=img)
    overlay = segmentation.mark_boundaries(img, new_labels)
    overlay = img_as_ubyte(overlay)
    return array_to_data_url(overlay)






if __name__ == '__main__':
    app.run_server(debug=True)
