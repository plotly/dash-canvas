# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SketchFieldDemo(Component):
    """A SketchFieldDemo component.
SketchFieldDemo is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- label (string; required): A label that will be printed when this component is rendered.
- value (string; optional): The value displayed in the input
- lineColor (string; optional): the color of the line
- filename (string; optional): The value displayed in the input

Available events: """
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, label=Component.REQUIRED, value=Component.UNDEFINED, lineColor=Component.UNDEFINED, filename=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'label', 'value', 'lineColor', 'filename']
        self._type = 'SketchFieldDemo'
        self._namespace = 'dash_canvas'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['id', 'label', 'value', 'lineColor', 'filename']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SketchFieldDemo, self).__init__(**args)

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
            return ('SketchFieldDemo(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'SketchFieldDemo(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
