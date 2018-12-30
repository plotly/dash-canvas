# dash-canvas

dash-canvas is a package for image processing with 
[Dash](https://dash.plot.ly/). It provides a Dash component for
annotating images, as well as utility functions for using such
annotations for various image processing tasks. 

Try out the 
[demo app for object segmentation](http://dash-canvas.herokuapp.com/) or the
[demo app for manual correction of segmentation](https://dash-canvas-separate.herokuapp.com/).

Get started with:
1. Install Dash and its dependencies: https://dash.plot.ly/installation
2. Run `python usage.py`
3. Visit http://localhost:8050 in your web browser

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

### Install dependencies


1. Install npm packages
    ```
    $ npm install
    ```
2. Create a virtual env and activate.
    ```
    $ virtualenv venv
    $ venv/Scripts/activate
    ```
    _Note: venv\Scripts\activate for windows_

3. Install python packages required to build components.
    ```
    $ pip install -r requirements.txt
    ```
4. Install the python packages for testing (optional)
    ```
    $ pip install -r tests/requirements.txt
    ```

