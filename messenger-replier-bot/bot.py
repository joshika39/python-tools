import zmq
from selection_picker_joshika39 import MenuWrapper, FunctionItem, SingleMenu
from constants import CLEAR, QUIT
from jsonlib.json_service import JsonService
from base import curr_dir
import os

def send_msg():
    p_id = input("Enter the conversation id (leave blank for predefined): ")
    if p_id == "":
        users_path = os.path.join(curr_dir(), 'users.json')
        json_service = JsonService(users_path)
        people = json_service.read('people')
        r = SingleMenu("Select a recepient:", [key for key in people.keys()]).show()
        selected = f"send-{people[r]}"
        socket.send(selected.encode("utf-8"))
        message = socket.recv()
        print(message)

def go_to_homepage():
    pass

def clear_logs():
    socket.send(CLEAR)
    message = socket.recv()
    print(message)

def exit_server():
    socket.send(QUIT)
    message = socket.recv()
    print(message)
    exit(0)


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://100.90.226.33:5555")

while True:
    MenuWrapper("Select a task:", [
        FunctionItem("Send message", send_msg),
        FunctionItem("Clear the logs", clear_logs),
        FunctionItem("Quit", exit_server)
    ]).show()
