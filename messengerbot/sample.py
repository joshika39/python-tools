from selenium.webdriver.chrome.options import Options
from jsonlib.json_service import JsonService
import os
import importlib
from botlib.base import proj_root
from botlib.selenium_lib import login, create_local
import conversations.factory
import sys
import time

users_path = os.path.join(proj_root(), 'users.json')

json_service = JsonService(users_path)

csenge_id = json_service.read('people/csenge')
joshua_id = json_service.read('people/joshua')

base_url = f"https://www.facebook.com/messages/t/{csenge_id}"

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2})
# option.set_capability("browserVersion", "99")


browser = login(base_url, create_local(driver_options=option))

while True:
    testers = JsonService(os.path.join(
        proj_root(), 'lists.json')).read("beta_testers")
    for module in list(sys.modules.values()):
        if "conversations" in module.__name__:
            importlib.reload(module)
    f = conversations.factory.ConversationFactory(json_service, base_url)
    chats = f.get_open_conversations(browser)
    for chat in chats:
        print(chat.display_str())

    for c in chats:
        if c.unread and c.id in testers:
            c.test()

    print("Refresh in 3 seconds")
    time.sleep(3)
