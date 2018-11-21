import numpy as np
import dash_canvas
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div([
    dash_canvas.DashCanvas(
        id='canvas',
        value=10,
        label='my-label',
        filename='file:///home/emma/travail/plotly/dash_canvas/camera.png'
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
	    accept='image/*'
	),

    dcc.Input(
    placeholder='Enter a value...',
    type='text',
    value='',
    id='filename'
    ),
    html.Div(id='output')
])

@app.callback(Output('filename', 'value'), [Input('canvas', 'JSON_string')])
def display_output(string):
    print(string)
    return None

@app.callback(Output('canvas', 'image_content'), [Input('upload-image', 'contents')])
def upload_image(string):
    return string


"""
@app.callback(Output('canvas', 'lineColor'), [Input('filename', 'value')])
def change_background(value):
    colors = ['red', 'black', 'blue', 'green']
    print(value)
    i = np.random.randint(0, 4)
    col = colors[i]
    return col
"""

if __name__ == '__main__':
    app.run_server(debug=True)
