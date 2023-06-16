from selenium.webdriver.chrome.options import Options
from jsonlib.json_service import JsonService 
import os
import importlib
from botlib.base import proj_root
from botlib.selenium_lib import login, create_local
import conversations.factory
import sys

smaple_msg = [
     "Hello my friend,",
     "",
     "The reason that you are getting this message is that you got enrolled to Joshua's beta tester program",
     "",
     "He is creating a replier and messenger manager bot. Thak you for sending a message to him.",
     "", 
     "God bless you!" 
]

users_path = os.path.join(proj_root(), 'users.json')

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

testers = JsonService(os.path.join(proj_root(), 'lists.json')).read("beta_testers")

print(testers)

browser = login(base_url, create_local(driver_options=option))

while True:
    input("press any key")
    for module in list(sys.modules.values()):
            if "conversations" in module.__name__:
                importlib.reload(module)
    f = conversations.factory.ConversationFactory(json_service, base_url)
    chats = f.get_open_conversations(browser)
    for chat in chats:
        print(chat.display_str())
        if chat.unread and chat.id in testers:
             chat.reply(smaple_msg)
