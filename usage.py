import numpy as np
import json
from skimage import io

import dash_canvas
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from parse_json import parse_jsonstring
from image_processing_utils import watershed_segmentation
from plot_utils import image_with_contour

# Image to segment and shape parameters
filename = 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Mitochondria%2C_mammalian_lung_-_TEM_%282%29.jpg'
img = io.imread(filename, as_gray=True)
print(img.dtype)
height, width = img.shape
canvas_width = 400
canvas_height = int(height * canvas_width / width)
scale = canvas_width / width

# ------------------ App definition ---------------------

app = dash.Dash(__name__)

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


app.scripts.config.serve_locally = True
app.css.config.serve_locally = True


app.layout = html.Div([
    html.Div([
    html.Div([
    html.H2(children='Segmentation tool'),
    dcc.Markdown('''
        Paint on each object you want to segment
	then press the Save button to trigger the segmentation.
    '''),

     dash_canvas.DashCanvas(
        id='canvas',
        label='my-label',
        width=canvas_width,
	height=canvas_height,
        scale=scale,
        filename=filename,
    ),
     ], className="six columns"),
    html.Div([
    html.H2(children='Segmentation result'),
    dcc.Graph(
        id='segmentation',
        figure=image_with_contour(img, img>0)
	)
    ], className="six columns")],# Div
	className="row")
    ])

# ----------------------- Callbacks -----------------------------

@app.callback(Output('segmentation', 'figure'),
             [Input('canvas', 'json_data')])
def update_figure(string):
    mask = parse_jsonstring(string, shape=(height, width))
    seg = watershed_segmentation(img, mask)
    return image_with_contour(img, seg)


if __name__ == '__main__':
    app.run_server(debug=True)
