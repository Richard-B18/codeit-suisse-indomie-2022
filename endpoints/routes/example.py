import logging
import json

from flask import request, jsonify

from endpoints import app

logger = logging.getLogger(__name__)


@app.route('/example', methods=['GET'])
def example():
    output = {
        "data": 50,
    }

    return jsonify(output)
