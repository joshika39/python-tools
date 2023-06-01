from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from constants import *
from selenium_lib import *
from json_service import JsonService

def chat_is_profile(driver: WebDriver, chat_id: str) -> bool:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(f'https://www.facebook.com/{chat_id}')
    results = search_elements_by_class(driver, CONTENT_NOT_FOUND)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    if len(results) == 0:
        return True
    
    return False

def archive_chat(driver: WebDriver, allowed_amount: int):
    chats = search_elements_by_class(driver, CHATS)
    if len(chats) > allowed_amount:
        success = False
        old_chats = chats[-allowed_amount:]
        i = 0
        while i < len(old_chats) and len(chats) > allowed_amount:
            chat = old_chats[-1]
            try:
                hover = ActionChains(driver).move_to_element(chat)
                hover.perform()
                context_menu = search_child_elements_by_xpath(chat, CONTEXT_MENU)
                if len(context_menu) > 0:
                    context_menu[0].click()
                    menu_items = search_elements_by_class(driver, MENU_ITEMS)
                    if len(menu_items) == SELF_OPTIONS["len"]:
                        menu_items[SELF_OPTIONS["click"]].click()
                    elif len(menu_items) == GROUP_OPTIONS["len"]:
                        menu_items[GROUP_OPTIONS["click"]].click()
                    elif len(menu_items) == SELF_OPTIONS["len"]:
                        menu_items[SELF_OPTIONS["click"]].click()
                else:
                    print("Context menu not found!")
            except StaleElementReferenceException as e:
                chats = search_elements_by_class(driver, CHATS)
                if len(chats) > allowed_amount:
                    old_chats = chats[-allowed_amount:]
                success = False
            except Exception as e:
                success = False
                print(f"Could not open menu: {e}")
            finally:
                if success:
                    i += 1

def get_unread_chats(driver: WebDriver, service: JsonService) -> dict:
    chats = search_elements_by_class(driver, CHATS)
    unread_users = {}  #type: dict
    registered_users = service.read("conversations")
    testers = service.read("beta_testers")
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
            if id not in registered_users:
                is_person = chat_is_profile(driver, id)
                if is_person:
                    user = {"type" : "person"}
                    registered_users[id] = user
                else:
                    user = {"type" : "group"}
                    registered_users[id] = user
            else:
                user = registered_users[id]
            
            child = search_child_elements_by_xpath(chat, READ_MSG)
            if len(child) > 0 and id in testers:
                unread_users[id] = user
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
    service.write("conversations", registered_users)   
    return unread_users


class ChatBox():
    pass


