import logging
import json

from flask import request, jsonify

from endpoints import app

logger = logging.getLogger(__name__)

@app.route('/square/', methods=["GET"])
def test():
    return "Result"

@app.route('/square/compute', methods=['POST'])
def solve():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return jsonify(result)

