from selenium.webdriver.chrome.options import Options
from jsonlib.json_service import JsonService
from base import curr_dir
from selenium_lib import login, connect_to_container, create_local
from selenium.webdriver.chrome.webdriver import WebDriver
import conversations.factory
import os
from constants import QUIT, CLEAR, SUCCESS
from zmq import Socket
import importlib
from response import Response
import sys
import zmq
import time

def do_action(driver: WebDriver, s: Socket, factory: conversations.factory.ConversationFactory):
    message = s.recv_pyobj()
    msg_str = message.decode("utf-8")
    print(f"Received request: {message}")
    if message == CLEAR:
        os.system('cls')
        r = Response()
        r.set_response("Cleared")
        s.send_pyobj(r)
    elif message == QUIT:
        driver.quit()
        s.send(SUCCESS)
        exit(0)
    elif "send-" in msg_str:
        c_id = msg_str.replace("send-", "")
        person = factory.create_conversation(driver, c_id)
        person.reply(["Szia Csenge, ", "", "Nagyon szeretlek!"])
        s.send(SUCCESS)

users_path = os.path.join(curr_dir(), 'users.json')

json_service = JsonService(users_path)

csenge_id = json_service.read('people/csenge')
joshua_id = json_service.read('people/joshua')

base_url = f"https://www.facebook.com/messages/t/{csenge_id}"

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
# option.set_capability("browserVersion", "99")
browser = login(base_url, create_local(driver_options=option))

# while True:
#     input("press any key")
#     for module in list(sys.modules.values()):
#             if "conversations" in module.__name__:
#                 importlib.reload(module)
#     f = conversations.factory.ConversationFactory(json_service, base_url)
#     chats = f.get_open_conversations(browser)
#     for chat in chats:
#         print(chat.display_str())
#         chat.save()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://100.90.226.33:5555")

while True:
    do_action(browser, socket, conversations.factory.ConversationFactory(json_service, base_url))
    time.sleep(2)

    

# conversations = factory.create_conversations(None)

# for c in conversations:
#     c.save()
# josh = factory.create_user(None, joshua_id)
# josh.reply(MSG_HU)

# test.reply(TEST_MSG)

# input('Press anything to end...')