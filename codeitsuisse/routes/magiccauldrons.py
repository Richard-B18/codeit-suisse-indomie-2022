from flask import Flask, request, jsonify
app = Flask(__name__)

def solvePart1(flowRate, time, row, col, mode=100):
    k = (flowRate * time) / mode
    row += 1
    col += 1
    gl = [[k]]
    level = 1
    overflow_occured = True
    while overflow_occured:   # also can stop when at needed row
        #print(gl[level-1])  #before overflow
        level += 1
        overflow_occured = False
        gl.append([0]*level)
        for i in range(level - 1):
            t = gl[level-2][i] - 1  # t is the remainder
            if t > 0:
                gl[level-1][i] += t/2   # add half of the remainder
                gl[level-1][i+1] += t/2
                gl[level-2][i] = 1
                overflow_occured = True
    #print(gl)  #after all
    if mode == 100:
        return format(gl[row-1][col-1] * mode, '.2f')
    return gl[row - 1][col - 1]

# def solvePart2(flowRate, amount, row, col):

@app.route('/magiccauldrons', methods=["GET", "POST"])
def solveThisShit():
    data = request.get_json()
    returnArr = []
    for dataObj in data:
        obj = {"part1": None, "part2": None, "part3": None, "part4": None}
        obj["part1"] = solvePart1(dataObj["part1"]["flow_rate"], dataObj["part1"]["time"], dataObj["part1"]["row_number"], 
        dataObj["part1"]["col_number"], 100)
        returnArr.append(obj)
    return jsonify(returnArr)

# print(solvePart1(23, 1, 0, 0, 100))