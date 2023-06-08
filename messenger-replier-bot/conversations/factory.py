from conversations.imports import *
from conversations.conversation import Conversation
from conversations.group import Group
from conversations.person import Person

class ConversationFactory():
    def __init__(self, service: JsonService, fallback_url: str) -> None:
        self.fallback_url = fallback_url
        self.service = service
        self.conversations = service.read("conversations")

    def create_conversation(self, driver: WebDriver, c_id: str) -> Conversation:
        conversation = self.service.read(f"conversations/{c_id}")
        is_open = False
        if "keep_open" in conversation.keys():
            is_open = conversation["keep_open"]
        result = None #type: Conversation
        match conversation["type"]:
            case "group":
                result = Group(self.service, driver, self.fallback_url, is_open, c_id)
            case "person":
                result = Person(self.service, driver, self.fallback_url, is_open, c_id)
        return result

    def create_conversations(self, driver: WebDriver) -> list[Conversation]:
        return_list = []  #type: list[Conversation]
        for conversation_id in self.conversations:
            return_list.append(self.create_conversation(driver, conversation_id))
                    
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