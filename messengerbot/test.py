import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5557")


for i in range(10):
    j = json.dumps({"num" : i + 1})
    socket.send_json({"num" : i + 1})