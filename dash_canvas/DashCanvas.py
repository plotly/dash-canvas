# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashCanvas(Component):
    """A DashCanvas component.
A canvas component for drawing on a background image and selecting
regions.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- className (string; optional): className of the parent div
- label (string; required): A label that will be printed when this component is rendered.
- image_content (string; optional): Image data
- width (number; optional): The width of the canvas
- height (number; optional): The height of the canvas
- scale (number; optional): Scaling factor of image
- lineWidth (number; optional): Width of drawing line
- lineColor (string; optional): Color of drawing line
- filename (string; optional): Name of image file to load
- trigger (number; optional): Bla
- json_data (string; optional): Sketch content as JSON string

Available events: """
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, label=Component.REQUIRED, image_content=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, scale=Component.UNDEFINED, lineWidth=Component.UNDEFINED, lineColor=Component.UNDEFINED, filename=Component.UNDEFINED, trigger=Component.UNDEFINED, json_data=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'label', 'image_content', 'width', 'height', 'scale', 'lineWidth', 'lineColor', 'filename', 'trigger', 'json_data']
        self._type = 'DashCanvas'
        self._namespace = 'dash_canvas'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['id', 'className', 'label', 'image_content', 'width', 'height', 'scale', 'lineWidth', 'lineColor', 'filename', 'trigger', 'json_data']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in [u'label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashCanvas, self).__init__(**args)

    def __repr__(self):
        if(any(getattr(self, c, None) is not None
               for c in self._prop_names
               if c is not self._prop_names[0])
           or any(getattr(self, c, None) is not None
                  for c in self.__dict__.keys()
                  if any(c.startswith(wc_attr)
                  for wc_attr in self._valid_wildcard_attributes))):
            props_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self._prop_names
                                      if getattr(self, c, None) is not None])
            wilds_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self.__dict__.keys()
                                      if any([c.startswith(wc_attr)
                                      for wc_attr in
                                      self._valid_wildcard_attributes])])
            return ('DashCanvas(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'DashCanvas(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
