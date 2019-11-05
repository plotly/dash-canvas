from __future__ import print_function as _

import os as _os
import sys as _sys
import json

import dash as _dash

# noinspection PyUnresolvedReferences
from ._imports_ import *
from ._imports_ import __all__

if not hasattr(_dash, 'development'):
    print('Dash was not successfully imported. '
          'Make sure you don\'t have a file '
          'named \n"dash.py" in your current directory.', file=_sys.stderr)
    _sys.exit(1)

_basepath = _os.path.dirname(__file__)
_filepath = _os.path.abspath(_os.path.join(_basepath, 'package.json'))
with open(_filepath) as f:
    package = json.load(f)

package_name = package['name'].replace(' ', '_').replace('-', '_')
__version__ = package['version']

_current_path = _os.path.dirname(_os.path.abspath(__file__))

_this_module = _sys.modules[__name__]

async_resources = [
    'canvas'
]

_js_dist = []

_js_dist.extend([{
        'relative_package_path': 'async~{}.js'.format(async_resource),
        'dev_package_path': 'async~{}.dev.js'.format(async_resource),
        'external_url': (
            'https://unpkg.com/dash-canvas@{}'
            '/dash_canvas/async~{}.js'
        ).format(__version__, async_resource),
        'namespace': 'dash_canvas',
        'async': True
    } for async_resource in async_resources])

_js_dist.extend([
    {
        'relative_package_path': 'dash_canvas.min.js',
        'dev_package_path': 'dash_canvas.dev.js',
        'namespace': package_name
    }
])

_css_dist = []


for _component in __all__:
    setattr(locals()[_component], '_js_dist', _js_dist)
    setattr(locals()[_component], '_css_dist', _css_dist)
