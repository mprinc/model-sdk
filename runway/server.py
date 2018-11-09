import base64
import io
from PIL import Image
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from .exceptions import RunwayError, MissingInputException


def deserialize_image(value):
    image = value[value.find(",")+1:]
    image = base64.decodestring(image)
    image = Image.open(io.BytesIO(image))
    return np.array(image)


def serialize_image(value):
    if type(value) is np.ndarray:
        im_pil = Image.fromarray(value)
    elif type(value) is Image.Image:
        im_pil = value
    buffer = io.BytesIO()
    im_pil.save(buffer, format='JPEG')
    return 'image/jpeg;base64,' + base64.b64encode(buffer.getvalue())


def deserialize(value, arg_type):
    if arg_type == 'text':
        return value
    elif arg_type == 'image':
        return deserialize_image(value)
    elif arg_type == 'number':
        return float(value)


def serialize(value, arg_type):
    if arg_type == 'text':
        return str(value)
    elif arg_type == 'image':
        return serialize_image(value)
    elif arg_type == 'number':
        return float(value)


class RunwayServer(object):
    def __init__(self, name):
        self.app = Flask(__name__)
        CORS(self.app)

        @self.app.route('/healthcheck')
        def healthcheck():
            return jsonify(message=name + ' running')

    def command(self, path, inputs=None, outputs=None):
        if inputs is None or outputs is None:
            raise Exception('You need to provide inputs and outputs for the command')
        def decorator(fn):
            @self.app.route('/' + path, methods=['POST'])
            def http_endpoint():
                try:
                    input_dict = request.json
                    for input_name, input_type in inputs.items():
                        if input_name not in input_dict:
                            raise MissingInputException(input_name)
                        input_dict[input_name] = deserialize(
                            input_dict[input_name], input_type)
                    output_dict = fn(input_dict)
                    for output_name, output_type in outputs.items():
                        output_dict[output_name] = deserialize(
                            output_dict[output_name], output_type)
                    return jsonify(output_dict)
                except RunwayError as err:
                    return jsonify(err.to_response())
            return fn
        return decorator

    def run(self, host='0.0.0.0', port=8000, threaded=True):
        self.app.run(host=host, port=port, threaded=threaded)
