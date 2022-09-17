import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def _manhattan(coor1, coor2):
    return abs(coor1[0] - coor2[0]) + abs(coor1[1] - coor2[1])


def _helper(current, target, direction):
    output = ''
    # target is down
    if current[0] < target[0]:
        if direction == 'N':
            output += 'RR'
        elif direction == 'W':
            output += 'L'
        elif direction == 'E':
            output += 'R'
        direction = 'S'

    # target is up
    if current[0] > target[0]:
        if direction == 'S':
            output += 'RR'
        elif direction == 'W':
            output += 'R'
        elif direction == 'E':
            output += 'L'
        direction = 'N'

    output += abs(current[0] - target[0]) * 'S'

    # target is left
    if current[1] < target[1]:
        if direction == 'N':
            output += 'R'
        elif direction == 'W':
            output += 'RR'
        elif direction == 'S':
            output += 'L'
        direction = 'E'

    # target is right
    if current[1] > target[1]:
        if direction == 'N':
            output += 'L'
        elif direction == 'E':
            output += 'RR'
        elif direction == 'S':
            output += 'R'
        direction = 'W'

    output += abs(current[1] - target[1]) * 'S'

    output += 'P'
    return direction, output


@app.route('/travelling-suisse-robot', methods=['POST'])
def travelling_suisse_robot():
    data = request.get_data(as_text=True)
    logger.error(data)

    h = {}
    s = 'CODEITSUISSE'
    special = ['S', 'E', 'I']

    arr = data.split('\n')

    if not arr[-1]:
        del arr[-1]

    for r in range(len(arr)):
        for c in range(len(arr[0])):
            if arr[r][c] != ' ':
                if arr[r][c] in h:
                    h[arr[r][c]].append([r,c,False])
                else:
                    h[arr[r][c]] = [[r,c,False]]

    output = ""

    pos = h['X'][0]
    direction = 'N'

    for c in s:
        coordinate = None
        if c in special:
            coordinates = h[c]

            closest = float('inf')

            visited = None
            for i in range(len(coordinates)):
                if h[c][i][2]:
                    continue
                coor = coordinates[i]
                d = _manhattan(pos, coor)
                if d < closest:
                    coordinate = coor
                    closest = d
                    visited = i
            h[c][visited][2] = True

        else:
            coordinate = h[c][0]

        direction, temp = _helper(pos, coordinate, direction)
        pos = coordinate
        output += temp
    return output



