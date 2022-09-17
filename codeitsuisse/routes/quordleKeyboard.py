import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/quordleKeyboard', methods=['POST'])
def quordleKeyboard():
    l = ["" for _ in range(26)]


    data = request.get_json()
    answers = data.get('answers')
    attempts = data.get('attempts')
    numbers = data.get('numbers')

    guessed = set()

    for i in range(len(attempts)):
        attempt = attempts[i]
        for c in set(attempt):
            if c not in guessed:
                l[ord(c) - ord('A')] = str(len(attempts) - i)
                guessed.add(c)

    output = {}

    output['part1'] = ''.join(l)

    part2 = ''
    n = ['' for _ in range(5)]
    for i in range(len(numbers)):
        if str(numbers[i]) in output['part1']:
            n[i // 5] += '1'
        else:
            n[i//5] += '0'

    logger.info(n)

    for i in n:
        part2 += chr(ord('A') + int(i, 2))

    for i in range(len(l)):
        if not l[i]:
            part2 += chr(ord('A') + i)

    output['part2'] = part2
    return json.dumps(output)




