from typing import Any
from conversations.imports import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from constants import CHATS, CHAT_LINK, READ_MSG, CONTEXT_MENU, MENU_ITEMS, CHAT_NAME, UCHAT_NAME

class Conversation():
    def __init__(self, service: JsonService, driver: WebDriver, home_url: str, id: str) -> None:
        self.service = service
        self.id = id
        self.home_url = home_url 
        self.driver = driver
        self.full_url = f'https://www.facebook.com/messages/t/{self.id}'
        self.__init_details()

    def refresh_element(self):
        chats = search_elements_by_class(self.driver, CHATS)
        i = 0
        found = False
        while i < len(chats) and not found:
            success = False
            chat = chats[i]
            try:
                # if not chat.is_displayed():
                #     self.driver.execute_script("document.querySelector(div[class='x78zum5 xdt5ytf x1iyjqo2 x5yr21d x6ikm8r x10wlt62']).scrollTop=500")
                link_elem = search_child_elements_by_xpath(chat, CHAT_LINK)[0]
                full_link = link_elem.get_attribute("href")
                id = full_link.replace('https://www.facebook.com/messages/t/', '')[:-1]
                if id == self.id:
                    self.element = chat
                    found = True
                    child = search_child_elements_by_xpath(chat, READ_MSG)
                    if len(child) > 0:
                        self.unread = True
                    else:
                        self.unread = False
                success = True
            except StaleElementReferenceException as e:
                print("Refreshing chats....")
                chats = search_elements_by_class(self.driver, CHATS)
                success = False
            except Exception as e:
                print(f"Unhandled exception with chat crawling: {e}")
            finally:
                if success:
                    i += 1
        self.is_open = found
        if not found:
            self.element = None

    def get_safe_data(self, key: str) -> Any | None:
        return self.service.read(f"{id}/{key}")
        
    def __init_details(self):
        self.last_message = self.get_safe_data("last_message")
        self.keep_open = self.get_safe_data("keep_open") == True
        self.refresh_element()
        self.name = self.get_safe_data("name") or ""
        if self.element is not None and self.name == "":
            s_text = UCHAT_NAME if self.unread else CHAT_NAME
            targets = search_child_elements_by_class(self.element, s_text)
            if len(targets) > 0:
                self.name = targets[0].text
            else: 
                self.name = self.id
        

    def goto_chat(self):
        if self.driver.current_url != self.full_url:
            self.driver.get(self.full_url)

    def get_nth_msg(driver: WebDriver, count: int):
        messages = search_elements_by_class(driver, MESSAGE, tag='div')
        pass

    def verify_action(self):
        self.driver.implicitly_wait(3)
    
    def reply(self, messages: list[str]) -> bool:
        sent = False
        tries = 4
        self.goto_chat()
        messageBox = search_elements_by_class(self.driver, MSG_BOX, "p")
        if len(messageBox) <= 0:
            print("Could get message box")
            return
        messageBox = messageBox[0]
        while not sent and tries >= 0:
            try:
                sent = True
                for message in messages:
                    messageBox.send_keys(message + Keys.SHIFT + Keys.ENTER)
                messageBox.send_keys(Keys.ENTER)
                print(f"Message sent to: {self.id}")
            except Exception as e:
                sent = False
                print(f"Could not enter message: {e}")
            finally:
                    tries -= 1
        self.verify_action()
        self.driver.get(self.home_url)
        return sent

    def archive(self) -> list[WebElement] | bool:
        try:
            hover = ActionChains(self.driver).move_to_element(self.element)
            hover.perform()
            context_menu = search_child_elements_by_xpath(self.element, CONTEXT_MENU)
            if len(context_menu) > 0:
                context_menu[0].click()
                menu_items = search_elements_by_class(self.driver, MENU_ITEMS)
                return menu_items
            else:
                print("Context menu not found!")
        except StaleElementReferenceException as e:
            self.refresh_element()
        except Exception as e:
            print(f"Could not open menu: {e}")

        return False

    def display_str(self) -> str:
        return self.name

    def json_format(self) -> dict:
        pass

    def save(self):
        json_obj = self.json_format()
        self.service.write(f"conversations/{self.id}", json_obj)