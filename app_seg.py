import numpy as np
import json
from skimage import io
from PIL import Image


import dash_canvas
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from dash_canvas.utils.parse_json import parse_jsonstring
from dash_canvas.utils.image_processing_utils import segmentation_generic
from dash_canvas.utils.plot_utils import image_with_contour
from dash_canvas.utils.io_utils import image_string_to_PILImage

# Image to segment and shape parameters
filename = 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Mitochondria%2C_mammalian_lung_-_TEM_%282%29.jpg'
img = io.imread(filename, as_gray=True)
height, width = img.shape
canvas_width = 500
canvas_height = round(height * canvas_width / width)
scale = canvas_width / width


# ------------------ App definition ---------------------

app = dash.Dash(__name__)

server = app.server

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})



app.layout = html.Div([
    html.Div([
    html.Div([
    html.H2(children='Segmentation tool'),
    dcc.Markdown('''
        Draw on the picture to annotate each object 
	you want to segment, then press the Save button 
	to trigger the segmentation.
    '''),

     dash_canvas.DashCanvas(
        id='canvas',
        label='my-label',
        width=canvas_width,
	    height=canvas_height,
        scale=scale,
        filename=filename,
    ),
    dcc.Upload(
		id='upload-image',
		children=[
		    'Drag and Drop or ',
		    html.A('Select an Image')
		],
		style={
		    'width': '100%',
		    'height': '50px',
		    'lineHeight': '50px',
		    'borderWidth': '1px',
		    'borderStyle': 'dashed',
		    'borderRadius': '5px',
		    'textAlign': 'center'
		},
		accept='image/*',
	    ),
    dcc.Dropdown(
        id='algorithm',
        options=[
            {'label': 'Watershed', 'value': 'watershed'},
            {'label': 'Random Walker', 'value': 'random_walker'},
            {'label': 'Random Forest', 'value': 'random_forest'}
        ],
        value='watershed'
    ),
     ], className="six columns"),
    html.Div([
    html.H2(children='Segmentation result'),
    dcc.Graph(
        id='segmentation',
        figure=image_with_contour(img, img>0, shape=(height, width))
	)
    ], className="six columns")],# Div
	className="row")
    ])

# ----------------------- Callbacks -----------------------------

@app.callback(Output('segmentation', 'figure'),
             [Input('canvas', 'image_content'),
              Input('canvas', 'json_data'),
              Input('canvas', 'height')],
             [State('canvas', 'scale'),
              State('canvas', 'width'),
	      State('algorithm', 'value')])
def update_figure_upload(image, string, h, s, w, algorithm):
    mask = parse_jsonstring(string, shape=(round(h/s), round(w/s)))
    if mask.sum() > 0:
        if image is None:
            im = img
            image = img
        else:
            im = image_string_to_PILImage(image)
            im = np.asarray(im)
        seg = segmentation_generic(im, mask, mode=algorithm)
    else:
        if image is None:
            image = img
        seg = np.zeros((h, w))
    return image_with_contour(image, seg, shape=(round(h/s), round(w/s)))



@app.callback(Output('canvas', 'image_content'),
             [Input('upload-image', 'contents')])
def update_canvas_upload(image_string):
    if image_string is None:
        raise ValueError
    if image_string is not None:
        return image_string
    else:
        return None


@app.callback(Output('canvas', 'height'),
             [Input('upload-image', 'contents')],
             [State('canvas', 'width'),
              State('canvas', 'height')])
def update_canvas_upload_shape(image_string, w, h):
    if image_string is None:
        raise ValueError
    if image_string is not None:
        # very dirty hack, this should be made more robust using regexp
        im = image_string_to_PILImage(image_string)
        im_h, im_w = im.height, im.width
        return round(w / im_w * im_h)
    else:
        return canvas_height


@app.callback(Output('canvas', 'scale'),
             [Input('upload-image', 'contents')])
def update_canvas_upload_scale(image_string):
    if image_string is None:
        raise ValueError
    if image_string is not None:
        # very dirty hack, this should be made more robust using regexp
        im = image_string_to_PILImage(image_string)
        im_h, im_w = im.height, im.width
        return canvas_width / im_w
    else:
        return scale







if __name__ == '__main__':
    app.run_server(debug=True)
