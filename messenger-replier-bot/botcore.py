from selenium.webdriver.chrome.options import Options
from jsonlib.json_service import JsonService
from base import curr_dir
from selenium_lib import login, connect_to_container, create_local
from selenium.webdriver.chrome.webdriver import WebDriver
from conversations.factory import ConversationFactory
import os
from constants import MSG_HU, TEST_MSG, QUIT, CLEAR, SUCCESS, ERROR
from zmq import Socket
import zmq
import time

def do_action(driver: WebDriver, s: Socket, factory: ConversationFactory):
    message = s.recv()
    msg_str = message.decode("utf-8")
    print(f"Received request: {message}")
    if message == CLEAR:
        os.system('cls')
        s.send(SUCCESS)
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

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://100.90.226.33:5555")

while True:
    do_action(browser, socket, ConversationFactory(json_service, base_url))
    time.sleep(2)

    

# conversations = factory.create_conversations(None)

# for c in conversations:
#     c.save()
# josh = factory.create_user(None, joshua_id)
# josh.reply(MSG_HU)

# test.reply(TEST_MSG)

# input('Press anything to end...')