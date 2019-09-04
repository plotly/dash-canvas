import json

from skimage import img_as_ubyte
import numpy as np

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

import dash_canvas
from dash_canvas.utils import array_to_data_url


def _get_button_by_title(dash_duo, title):
    return dash_duo.wait_for_element(
        'button[title="{}"]'.format(title)
    )


def test_canvas_undo_redo(dash_duo):
    h, w = 10, 10
    overlay = np.zeros((h, w), dtype=np.uint8)
    overlay = img_as_ubyte(overlay)

    # Set up a small app. This could probably be made into a fixture.
    app = dash.Dash(__name__)
    app.layout = html.Div([
        dcc.Store(id='cache', data=''),
        dash_canvas.DashCanvas(
            id="canvas",
            width=w,
            height=h,
            image_content=array_to_data_url(overlay),
            goButtonTitle="save"
        )
    ])

    data_saved = []

    @app.callback(
        Output('cache', 'data'),
        [Input("canvas", "trigger")],
        [State("canvas", "json_data")]
    )
    def update_overlay(flag, data):
        data_saved.append(data)

    dash_duo.start_server(app)

    # At application startup, a black 10x10 image is shown. When we click
    # save, we expect a non-trivial JSON object representing this image. We
    # assert that we get this object, but we don't dig into it.
    btn = _get_button_by_title(dash_duo, "Save")
    btn.click()

    objs_1 = json.loads(data_saved[-1])['objects']
    assert len(objs_1) > 0

    # When we click "undo", the image disappears. We check that we get an
    # empty JSON representation back.
    btn = _get_button_by_title(dash_duo, "Undo")
    btn.click()
    btn = _get_button_by_title(dash_duo, "Save")
    btn.click()

    objs_2 = json.loads(data_saved[-1])['objects']
    assert objs_2 == []

    # When we click "redo", the original 10x10 black image is restored.
    btn = _get_button_by_title(dash_duo, "Redo")
    btn.click()
    btn = _get_button_by_title(dash_duo, "Save")
    btn.click()

    objs_3 = json.loads(data_saved[-1])['objects']
    assert objs_1 == objs_3
