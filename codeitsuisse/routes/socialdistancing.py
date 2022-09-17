from copy import deepcopy

import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def rec(hash, n):
    count = 0
    # n is people remaining
    if n > len(hash):
        return 0

    if n == 0:
        return 1

    for k, v in hash.items():
        temp = deepcopy(hash)

        del temp[k]

        r, c = k
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (r + i, c + j) in temp:
                    del temp[(r + i, c + j)]
        count += rec(temp, n - 1)

    return count

@app.route('/social-distancing', methods=['POST'])
def ans():
    datas = request.get_json()

    result = []

    for data in datas:
        data = data.split(', ')
        M = int(data[0])
        N = int(data[1])

        num = int(data[2])


        occupiedseats = []
        for i in range(3, len(data), 2):
            occupiedseats.append((int(data[i]), int(data[i + 1])))


        x = [[True for i in range(M)] for j in range(N)]
        # find the valid seating arrangement
        for i in range(len(occupiedseats)):
            r = occupiedseats[i][0]
            c = occupiedseats[i][1]
            x[r][c] = False

            for j in range(-1, 2):
                for k in range(-1, 2):
                    if r + j >= 0 and r + j < N and c + k >= 0 and c + k < M:
                        x[r + j][c + k] = False

        # creating hash to keep all the valid position for movement
        hash = {}
        indexc = 0
        indexr = 0
        for i in x:
            for j in i:
                if j == True:
                    hash[(indexc, indexr)] = True
                indexr += 1
            indexr = 0
            indexc += 1

        # checking whether the locations in the hash are valid relative to each other
        # code
        numofpeople = num - len(occupiedseats)

        output = rec(hash, numofpeople)
        if output == 0:
            result.append("No Solution")
        else:
            result.append(output)

    return jsonify(result)