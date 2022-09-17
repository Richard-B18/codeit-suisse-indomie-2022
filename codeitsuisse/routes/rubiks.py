import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/rubiks', methods=['POST'])
def rubiks():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    ops = data["ops"]
    state = data["state"]
    for i in range(0,len(ops)):
        if ops[i] == "U":
            if i < len(ops) - 1 and ops[i+1]=="i":
                state = Ui(state)
            else:
                state = U(state)
        elif ops[i] == "F":
            if i < len(ops) - 1 and ops[i+1]=="i":
                state = Fi(state)
            else:
                state = F(state)
        elif ops[i] == "D":
            if i < len(ops) - 1 and ops[i+1]=="i":
                state = Di(state)
            else:
                state = D(state)
        elif ops[i] == "B":
            if i < len(ops) - 1 and ops[i+1]=="i":
                state = Bi(state)
            else:
                state = B(state)
        elif ops[i] == "L":
            if i < len(ops) - 1 and ops[i+1]=="i":
                state = Li(state)
            else:
                state = L(state)
        elif ops[i] == "R":
            if i < len(ops) - 1 and ops[i+1]=="i":
                state = Ri(state)
            else:
                state = R(state)
    return json.dumps(state)

def R(state):
    for i in range(0,3):
        state["f"][i][2],state["u"][i][2],state["b"][2-i][0],state["d"][i][2] = state["d"][i][2],state["f"][i][2],state["u"][i][2],state["b"][2-i][0]
    state["r"] = Rotate_Clockwise(state["r"])
    return state

def Ri(state):
    for i in range(0,3):
        state["f"][i][2],state["u"][i][2],state["b"][2-i][0],state["d"][i][2] = state["u"][i][2],state["b"][2-i][0],state["d"][i][2],state["f"][i][2]
    state["r"] = Rotate_Anti_Clockwise(state["r"])
    return state

def L(state):
    for i in range(0,3):
        state["f"][i][0],state["u"][i][0],state["b"][2-i][2],state["d"][i][0] = state["u"][i][0],state["b"][2-i][2],state["d"][i][0],state["f"][i][0]
    state["l"] = Rotate_Clockwise(state["l"])
    return state

def Li(state):
    for i in range(0,3):
        state["f"][i][0],state["u"][i][0],state["b"][2-i][2],state["d"][i][0] = state["d"][i][0],state["f"][i][0],state["u"][i][0],state["b"][2-i][2]
    state["l"] = Rotate_Anti_Clockwise(state["l"])
    return state

def U(state):
    state["f"][0],state["l"][0],state["b"][0],state["r"][0] = state["r"][0], state["f"][0], state["l"][0], state["b"][0]
    state["u"] = Rotate_Clockwise(state["u"])
    return state

def Ui(state):
    state["f"][0],state["l"][0],state["b"][0],state["r"][0] = state["l"][0], state["b"][0], state["r"][0], state["f"][0]
    state["u"] = Rotate_Anti_Clockwise(state["u"])
    return state

def Di(state):
    state["f"][2],state["l"][2],state["b"][2],state["r"][2] = state["r"][2], state["f"][2], state["l"][2], state["b"][2]
    state["d"] = Rotate_Anti_Clockwise(state["d"])
    return state

def D(state):
    state["f"][2],state["l"][2],state["b"][2],state["r"][2] = state["l"][2], state["b"][2], state["r"][2], state["f"][2]
    state["d"] = Rotate_Clockwise(state["d"])
    return state

def F(state):
    for i in range(0,3):
        state["u"][2][i],state["r"][i][0],state["d"][0][2-i],state["l"][i][2] = state["l"][i][2],state["u"][2][i],state["r"][i][0],state["d"][0][2-i]
    state["f"] = Rotate_Clockwise(state["f"])
    return state

def Fi(state):
    for i in range(0,3):
        state["u"][2][i],state["r"][i][0],state["d"][0][2-i],state["l"][i][2] = state["r"][i][0],state["d"][0][2-i],state["l"][i][2],state["u"][2][i],
    state["f"] = Rotate_Anti_Clockwise(state["f"])
    return state

def Bi(state):
    for i in range(0,3):
        state["u"][0][i],state["r"][i][2],state["d"][2][2-i],state["l"][i][0] = state["l"][i][0],state["u"][0][i],state["r"][i][2],state["d"][2][2-i]
    state["b"] = Rotate_Anti_Clockwise(state["b"])
    return state

def B(state):
    for i in range(0,3):
        state["u"][0][i],state["r"][i][2],state["d"][2][2-i],state["l"][i][0] = state["r"][i][2],state["d"][2][2-i],state["l"][i][0],state["u"][0][i],
    state["b"] = Rotate_Clockwise(state["b"])
    return state

def Rotate_Clockwise(m):
    m[0][0],m[0][1],m[0][2],m[1][0],m[1][2],m[2][0],m[2][1],m[2][2] = m[2][0],m[1][0],m[0][0],m[2][1],m[0][1],m[2][2],m[1][2],m[0][2]
    return m

def Rotate_Anti_Clockwise(m):
    m[0][0],m[0][1],m[0][2],m[1][0],m[1][2],m[2][0],m[2][1],m[2][2] = m[0][2],m[1][2],m[2][2],m[0][1],m[2][1],m[0][0],m[1][0],m[2][0]
    return m