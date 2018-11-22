import numpy as np
import json
import dash_canvas
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from parse_json import parse_jsonstring
from image_processing_utils import watershed_segmentation
from skimage import io
import plotly.graph_objs as go

filename = 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Mitochondria%2C_mammalian_lung_-_TEM_%282%29.jpg'
img = io.imread(filename, as_gray=True)
height, width = img.shape

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div([
    html.H1(children='Image segmentation tool'),

    html.Div(children='''
        Paint on each object you want to segment \n, 
	then press the Save button to trigger the segmentation.
    '''),
    dash_canvas.DashCanvas(
        id='canvas',
        label='my-label',
        width=width,
	height=height,
        filename=filename
    ),
     dcc.Upload(
	    id='upload-image',
	    children=[
		'Drag and Drop or ',
		html.A('Select an Image')
	    ],
	    style={
		'width': '30%',
		'height': '50px',
		'lineHeight': '50px',
		'borderWidth': '1px',
		'borderStyle': 'dashed',
		'borderRadius': '5px',
		'textAlign': 'center'
	    },
	    accept='image/*'
	),

    dcc.Input(
    placeholder='Enter a value...',
    type='text',
    value='',
    id='filename'
    ),
    html.Div(id='output'),
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

])


@app.callback(Output('segmentation', 'figure'), [Input('canvas', 'json_data')])
def update_figure(string):
    print(string)
    mask = parse_jsonstring(string, shape=(height, width))
    seg = watershed_segmentation(img, mask)
    return {'data': [
                go.Heatmap(
                    z=img, colorscale='Greys'
                    ),
                go.Contour(
                    z=seg,
                    contours=dict(
                                coloring='lines',)
                )
                ],
            'layout': dict(width=width, height=height, yaxis=dict(
                                            autorange='reversed'))

    }
 


@app.callback(Output('filename', 'value'), [Input('canvas', 'json_data')])
def display_output(string):
    fp = open('data.json', 'w')
    json.dump(string, fp)
    fp.close()
    return None

@app.callback(Output('canvas', 'image_content'), [Input('upload-image', 'contents')])
def upload_image(string):
    return string


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


if __name__ == '__main__':
    app.run_server(debug=True)
