import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from glob import glob
import base64
import dash

import app1_seg as app1
import app2_correct_segmentation as app2
import app3_background_removal as app3
import app4_measure_length as app4
import app5_stitching as app5

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

apps = {'app1': app1, 'app2': app2, 'app3': app3, 'app4': app4,
        'app5': app5}

for key in apps:
    try:
        apps[key].callbacks(app)
    except AttributeError:
        continue


def demo_app_desc(name):
    """ Returns the content of the description specified in the app. """
    desc = ''
    try:
        desc = apps[name].description()
    except AttributeError:
        pass
    return desc


def demo_app_name(name):
    """ Returns a capitalized title for the app, with "Dash"
    in front."""
    desc = ''
    try:
        desc = apps[name].title()
    except AttributeError:
        pass
    return desc


def demo_app_link_id(name):
    """Returns the value of the id of the dcc.Link related to the demo app. 	  """
    return 'app-link-id-{}'.format(name)


def demo_app_img_src(name):
    """ Returns the base-64 encoded image corresponding
        to the specified app."""
    pic_fname = './app_pics/{}.png'.format(
        name
    )
    try:
        return 'data:image/png;base64,{}'.format(
              base64.b64encode(
                  open(pic_fname, 'rb').read()).decode())
    except Exception:
        return 'data:image/png;base64,{}'.format(
              base64.b64encode(
                  open('./assets/dashbio_logo.png', 'rb').read()).decode())



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname is not None and len(pathname) > 1 and pathname[1:] in apps.keys():
        app_name = pathname[1:]
        return html.Div(id="waitfor",
                          children=apps[app_name].layout,
                        )
    else:
        return html.Div(
            id='gallery-apps',
            children=[
                html.Div(className='gallery-app', children=[
                    dcc.Link(
                        children=[
                            html.Img(className='gallery-app-img',
                                     src=demo_app_img_src(name)),
                            html.Div(className='gallery-app-info',
                                children=[
                                    html.Div(className='gallery-app-name',
                                        children=[
                                            demo_app_name(name)
                                    ]),
                                    html.Div(className='gallery-app-desc',
                                        children=[demo_app_desc(name)
                                    ]),

                            ])
                        ],
                        id=demo_app_link_id(name),
                        href="/{}".format(
                            name.replace("app_", "").replace("_", "-")
                        )
                    )
                ]) for name in apps
            ])



server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
