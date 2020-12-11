# Runway Module

The Runway module exposes three simple functions that can be combined to expose your models to the Runway app using a simple interface.

- [`@runway.setup()`](#runway.setup): A [Python decorator](https://www.thecodeship.com/patterns/guide-to-python-function-decorators/) used to initialize and configure your model.
- [`@runway.command()`](#runway.command): A Python <span class='definition'>decorator</span> used to define the <span class='italic'>interface to your model</span>. Each command creates an <span class='important'>HTTP route</span> which can process user input and return outputs from the model.
- [`runway.run()`](#runway.run): The entrypoint function that <span class='important'>starts</span> the SDK's HTTP interface. It fires the function decorated by `@runway.setup()` and listens for commands on the network, forwarding them along to the appropriate functions decorated with `@runway.command()`.

## Reference
<!--
Because the runway/__init__.py file defines its functions via assignment from runway/model.py, we have to use this autofunction trick to make sure the function signatures show up correctly.
See https://stackoverflow.com/questions/5365684/is-it-possible-to-override-sphinx-autodoc-for-specific-functions/5368194#5368194
-->
```eval_rst
.. automodule:: runway

.. autofunction:: setup(decorated_fn=None, options=None)
.. autofunction:: command(name, inputs={}, outputs={})
.. autofunction:: run(host='0.0.0.0', port=9000, model_options={}, debug=False, meta=False)
```