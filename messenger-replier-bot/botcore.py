from selenium.webdriver.chrome.options import Options
from jsonlib.json_service import JsonService
from base import curr_dir
from selenium_lib import login, connect_to_container, create_local
from selenium.webdriver.chrome.webdriver import WebDriver
import conversations.factory
import os
from zmq import Socket
import importlib
from response import Response
from botaction import BotAction
import sys
import zmq
import time
import pickle

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
# browser = login(base_url, create_local(driver_options=option))

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
socket.bind("tcp://*:5555")
action = None
while action is None or not action.exit_after:
    action = socket.recv_pyobj()  #type: BotAction
    print(f"Action {action.name} arrived. Starting execution...")
    action.do_action()
    socket.send_pyobj(Response(True, "OK"))
    

# conversations = factory.create_conversations(None)

# for c in conversations:
#     c.save()
# josh = factory.create_user(None, joshua_id)
# josh.reply(MSG_HU)

# test.reply(TEST_MSG)

# input('Press anything to end...')