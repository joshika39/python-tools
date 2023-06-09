from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expected_conditions
from constants import *
from selenium_lib import *

def get_unread_chats(driver: WebDriver) -> dict:
    chats = search_elements_by_class(driver, CHATS)
    unread_users = {}  #type: dict
    i = 0
    while i < len(chats):
        success = False
        chat = chats[i]
        try:
            if not chat.is_displayed():
                driver.execute_script("document.querySelector(div[class='x78zum5 xdt5ytf x1iyjqo2 x5yr21d x6ikm8r x10wlt62']).scrollTop=500")
            link_elem = search_child_elements_by_xpath(chat, CHAT_LINK)[0]
            full_link = link_elem.get_attribute("href")
            id = full_link.replace('https://www.facebook.com/messages/t/', '')[:-1]
            child = search_child_elements_by_xpath(chat, READ_MSG)
            success = True
        except StaleElementReferenceException as e:
            print("Refreshing chats....")
            chats = search_elements_by_class(driver, CHATS)
            success = False
        except Exception as e:
            print(f"Unhandled exception with chat crawling: {e}")
        finally:
            if success:
                i += 1
    return unread_users


class ChatBox():
    pass


