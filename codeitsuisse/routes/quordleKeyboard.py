import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/quordleKeyboard', methods=['POST'])
def quordleKeyboard():
    data = request.get_json()
    answers = data.get('answers')
    attempts = data.get('attempts')
    numbers = data.get('numbers')

    logger.info(answers)
    logger.info(attempts)
    logger.info(numbers)




