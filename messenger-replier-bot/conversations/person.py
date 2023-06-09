from conversations.imports import *
from conversations.conversation import Conversation
from constants import CHAT_NAME

class Person(Conversation):
    def __init__(self, service: JsonService, driver: WebDriver, home_url: str, id: str) -> None:
        super().__init__(service, driver, home_url, id)
        self.__init_details()

    def __init_details(self):
        if self.element is not None:
            targets = search_child_elements_by_class(self.element, CHAT_NAME)
            if len(targets) > 0:
                self.displayed_name = targets[0].text
            else: 
                self.displayed_name = f"Person: {self.id} (name not found)"
        else:
            self.displayed_name = f"Person: {self.id} (not found)"
    
    def reply(self, messages: list[str]) -> bool:
        curr_time = date.today()
        if self.last_message is not None:
            last_time = datetime.strptime(self.last_message, "%Y-%m-%d")
            if curr_time == last_time:
                messages['Ma mar kaptal uzenetet', ' ', ' ', 'Peace out ( ´ ▽ ` )ﾉ']
        else:
            self.last_message = curr_time
        
        return super().reply(messages) 
    
    def archive(self):
        menu = super().archive()
        match len(menu):
            case 3:
                menu[1].click()
                return True
            case 9:
                menu[6].click()
                return True
        return False
                
    def json_format(self) -> dict:
        return {"type" : "person", "last_message" : self.last_message, "keep_open" : self.keep_open, "displayed_name": self.displayed_name}
    
