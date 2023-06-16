from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from jsonlib.json_service import JsonService
from botlib.selenium_lib import search_elements_by_class, search_child_elements_by_class, search_child_elements_by_xpath, search_elements_by_xpath, get_id_from_link
from botlib.constants import MSG_BOX, MESSAGE
from datetime import datetime, date