from conversations.conversation import Conversation
from conversations.group import Group
from conversations.person import Person
from botlib.constants import CONTENT_NOT_FOUND
from selenium.webdriver.chrome.webdriver import WebDriver
from botlib.selenium_lib import search_elements_by_class, search_elements_by_xpath, get_id_from_link
from jsonlib.json_service import JsonService


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


class ConversationFactory():
    def __init__(self, service: JsonService, fallback_url: str) -> None:
        self.fallback_url = fallback_url
        self.service = service
        self.conversations = service.read("conversations")

    def create_conversation(self, driver: WebDriver, c_id: str) -> Conversation:
        conversation = self.service.read(f"conversations/{c_id}")
        result = None #type: Conversation
        match conversation["type"]:
            case "group":
                result = Group(self.service, driver, self.fallback_url, c_id)
            case "person":
                result = Person(self.service, driver, self.fallback_url, c_id)
        return result
    
    def create_conversations(self, driver: WebDriver) -> list[Conversation]:
        return_list = []  #type: list[Conversation]
        for conversation_id in self.conversations:
            return_list.append(self.create_conversation(driver, conversation_id))
        return return_list
    
    def create_conversations_from_list(self, driver: WebDriver, ids: list[str]) -> list[Conversation]:
        return_list = []  #type: list[Conversation]
        for conversation_id in ids:
            result = None  #type: Conversation
            if conversation_id not in self.conversations:
                if chat_is_profile(conversation_id):
                    result = Person(self.service, driver, self.fallback_url, conversation_id)
                else:
                    result = Group(self.service, driver, self.fallback_url, conversation_id)
            else:
                result = self.create_conversation(driver, conversation_id)
            return_list.append(result)
        return return_list
    
    def get_open_conversations(self, driver: WebDriver) -> list[Conversation]:
        return_list = []  #type: list[Conversation]

        res = search_elements_by_xpath(driver, ["a", "role", "link"])
        ids = []
        for r in res:
            s, c_id = get_id_from_link(r)
            if s:
                ids.append(c_id)
        ids = ids[0:10]

        for conversation_id in ids:
            result = None  #type: Conversation
            if conversation_id not in self.conversations:
                if chat_is_profile(driver, conversation_id):
                    result = Person(self.service, driver, self.fallback_url, conversation_id)
                else:
                    result = Group(self.service, driver, self.fallback_url, conversation_id)
            else:
                result = self.create_conversation(driver, conversation_id)
            result.save()
            return_list.append(result)
        return return_list
    
    def create_user(self, driver: WebDriver, id: str) -> Conversation:
        if id not in self.conversations:
            user = {
                "type" : "person",
                "last_message": ""
            }
            self.conversations[id] = user
            self.service.write(f"conversations/{id}", user) 
        return Person(self.service, driver, self.fallback_url, id)

    def create_group(self, driver: WebDriver, id: str) -> Conversation:
        if id not in self.conversations:
            user = {
                "type" : "group",
                "last_message": ""
            }
            self.conversations[id] = user
            self.service.write(f"conversations/{id}", user) 
        return Group(self.service, driver, self.fallback_url, id)