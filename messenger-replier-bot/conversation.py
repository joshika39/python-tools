from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from json_service import JsonService
from selenium_lib import search_elements_by_class
from constants import MSG_BOX, MESSAGE
from datetime import datetime, date

class Conversation():
    def __init__(self, service: JsonService, driver: WebDriver, home_url: str, is_open: bool, id: str) -> None:
        self.service = service
        self.id = id
        self.home_url = home_url 
        self.driver = driver
        self.last_message = self.service.read(f"{id}/last_message")  #type: str
        self.full_url = f'https://www.facebook.com/messages/t/{self.id}'
        if is_open is None:
            self.keep_open = False
        else:
            self.keep_open = is_open

    def goto_chat(self):
        if self.driver.current_url != self.full_url:
            self.driver.get(self.full_url)

    def get_nth_msg(driver: WebDriver, count: int):
        messages = search_elements_by_class(driver, MESSAGE, tag='div')
        pass

    def verify_action(self):
        self.driver.implicitly_wait(3)

    def __reply_base(self, messages: list[str]) -> bool:
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
    
    def reply(self, messages: list[str]):
        pass

    def json_format(self) -> dict:
        pass

    def save(self):
        json_obj = self.json_format()
        self.service.write(f"conversations/{self.id}", json_obj)

class User(Conversation):
    def __init__(self, service: JsonService, driver: WebDriver, home_url: str, is_open: bool, id: str) -> None:
        super().__init__(service, driver, home_url, is_open, id)

    def reply(self, messages: list[str]) -> bool:
        curr_time = date.today()
        if self.last_message is not None:
            last_time = datetime.strptime(self.last_message, "%Y-%m-%d")
            if curr_time == last_time:
                messages['Ma mar kaptatok uzenetet', ' ', ' ', 'Peace out ( ´ ▽ ` )ﾉ']
        else:
            self.last_message = curr_time
        
        return self.__reply_base(messages) 
    
    def json_format(self) -> dict:
        return {"type" : "person", "last_message" : self.last_message, "keep_open" : self.keep_open}
    
class Group(Conversation):
    def __init__(self, service: JsonService, driver: WebDriver, home_url: str, is_open: bool, id: str) -> None:
        super().__init__(service, driver, home_url, is_open, id)

    def reply(self, messages: list[str]) -> bool:
        curr_time = date.today()
        if self.last_message is not None:
            last_time = datetime.strptime(self.last_message, "%Y-%m-%d")
            if curr_time == last_time:
                messages['Ma mar kaptatok uzenetet', ' ', ' ', 'Peace out ( ´ ▽ ` )ﾉ']
        else:
            self.last_message = curr_time
        
        return self.__reply_base(messages) 
    
    def json_format(self) -> dict:
        return {"type" : "group", "last_message" : self.last_message, "keep_open" : self.keep_open}

class ConversationFactory():
    def __init__(self, service: JsonService, fallback_url: str) -> None:
        self.fallback_url = fallback_url
        self.service = service
        self.conversations = service.read("conversations")

    def create_conversations(self, driver: WebDriver) -> list[Conversation]:
        return_list = []  #type: list[Conversation]
        for conversation_id in self.conversations:
            conversation = self.service.read(f"conversations/{conversation_id}")
            is_open = False
            if "keep_open" in conversation.keys():
                is_open = conversation["keep_open"]

            match conversation["type"]:
                case "group":
                    return_list.append(Group(self.service, driver, self.fallback_url, is_open, conversation_id))
                case "person":
                    return_list.append(User(self.service, driver, self.fallback_url, is_open, conversation_id))
                    
        return return_list
    
    def create_user(self, driver: WebDriver, id: str) -> Conversation:
        if id not in self.conversations:
            user = {
                "type" : "person",
                "last_message": ""
            }
            self.conversations[id] = user
            self.service.write(f"conversations/{id}", user) 
        return User(self.service, driver, self.fallback_url, id)

    def create_group(self, driver: WebDriver, id: str) -> Conversation:
        if id not in self.conversations:
            user = {
                "type" : "group",
                "last_message": ""
            }
            self.conversations[id] = user
            self.service.write(f"conversations/{id}", user) 
        return Group(self.service, driver, self.fallback_url, id)
