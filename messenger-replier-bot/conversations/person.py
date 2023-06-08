from conversations.imports import *
from conversations.conversation import Conversation

class Person(Conversation):
    def __init__(self, service: JsonService, driver: WebDriver, home_url: str, is_open: bool, id: str) -> None:
        super().__init__(service, driver, home_url, is_open, id)

    def reply(self, messages: list[str]) -> bool:
        curr_time = date.today()
        if self.last_message is not None:
            last_time = datetime.strptime(self.last_message, "%Y-%m-%d")
            if curr_time == last_time:
                messages['Ma mar kaptal uzenetet', ' ', ' ', 'Peace out ( ´ ▽ ` )ﾉ']
        else:
            self.last_message = curr_time
        
        return super().reply(messages) 
    
    def json_format(self) -> dict:
        return {"type" : "person", "last_message" : self.last_message, "keep_open" : self.keep_open}