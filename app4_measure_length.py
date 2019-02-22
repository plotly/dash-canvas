import numpy as np
import pandas as pd
from skimage import io

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table

import dash_canvas
from dash_canvas.utils.io_utils import (image_string_to_PILImage,
                                        array_to_data_url)
from dash_canvas.utils.parse_json import parse_jsonstring_line


def title():
    return "Measure lengths"

def description():
    return "Draw lines on objects to measure their lengths."


filename = 'https://upload.wikimedia.org/wikipedia/commons/a/a4/MRI_T2_Brain_axial_image.jpg'
img = io.imread(filename)[..., 0].T
height, width = img.shape
canvas_width = 600
canvas_height = round(height * canvas_width / width)
scale = canvas_width / width

list_columns = ['length', 'width', 'height']
columns = [{"name": i, "id": i} for i in list_columns]

layout = html.Div([
    html.Div([
        dash_canvas.DashCanvas(
            id='canvas-line',
            label='my-label',
            width=canvas_width,
            height=canvas_height,
            scale=scale,
            lineWidth=2,
            lineColor='red',
            tool='line',
            image_content=array_to_data_url(img),
            goButtonTitle='Measure',
            ),
    ], className="seven columns"),
    html.Div([
        html.H2('Draw lines and measure object lengths'),
        html.H4(children="Objects properties"),
        html.Div(id='sh_x', hidden=True),
        dash_table.DataTable(
            id='table-line',
            columns=columns,
            editable=True,
            )
    ], className="four columns"),
    ])


def callbacks(app):

    @app.callback(Output('table-line', 'data'),
                  [Input('canvas-line', 'json_data')])
    def show_string(string):
        props = parse_jsonstring_line(string)
        df = pd.DataFrame(props, columns=list_columns)
        return df.to_dict("records")
