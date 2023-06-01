from selenium.webdriver.chrome.options import Options
from json_service import JsonService
from base import curr_dir
from selenium_lib import login
from conversation import ConversationFactory
import os
from constants import MSG_HU, TEST_MSG

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

# browser = login(base_url, option)
factory = ConversationFactory(json_service, base_url)

# josh = factory.create_user(None, joshua_id)
# josh.reply(MSG_HU)
test = factory.create_user(None, "123234345")
# test.reply(TEST_MSG)

# input('Press anything to end...')