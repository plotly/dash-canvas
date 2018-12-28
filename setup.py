import json
import os
from setuptools import setup


with open(os.path.join('dash_canvas', 'package.json')) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")


setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    url='https://github.com/plotly/dash-canvas',
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package['description'] if 'description' in package else package_name,
    install_requires=['dash', 'dash-html-components', 'scikit-image', 'Pillow']
)
