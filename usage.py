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

# Image to segment and shape parameters
filename = 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Mitochondria%2C_mammalian_lung_-_TEM_%282%29.jpg'
img = io.imread(filename, as_gray=True)
height, width = img.shape


# ------------------ App definition ---------------------

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div([
     html.Div([
     html.H1(children='Image segmentation tool'),

     dcc.Markdown('''
        Paint on each object you want to segment
	then press the Save button to trigger the segmentation.
    '''),

     dash_canvas.DashCanvas(
        id='canvas',
        label='my-label',
        width=width,
	height=height,
        filename=filename
    ),
    ]),

    html.Div([
    html.H1(children='Segmentation result'),
    dcc.Graph(
        id='segmentation',
	figure={
            'data': [
                go.Heatmap(
                    z=img, colorscale='Greys'
                    )
                ],
            'layout': dict(width=width, height=height,
                yaxis=dict(autorange='reversed'))
            }

	)
	])],# Div

	className='row')

# ----------------------- Callbacks -----------------------------

@app.callback(Output('segmentation', 'figure'),
             [Input('canvas', 'json_data')])
def update_figure(string):
    mask = parse_jsonstring(string, shape=(height, width))
    seg = watershed_segmentation(img, mask)
    return {'data': [
                go.Heatmap(
                    z=img, colorscale='Greys'
                    ),
                go.Contour(
                    z=seg,
                    contours=dict(coloring='lines',),
                    line=dict(width=3)
                )
                ],
            'layout': dict(width=width, height=height,
                            yaxis=dict(autorange='reversed'))

    }


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


if __name__ == '__main__':
    app.run_server(debug=True)
