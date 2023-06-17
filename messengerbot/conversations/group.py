from conversations.imports import *
from conversations.conversation import Conversation
from botlib.constants import CHAT_NAME

class Group(Conversation):
    def __init__(self, service: JsonService, driver: WebDriver, home_url: str, id: str) -> None:
        super().__init__(service, driver, home_url, id)

    def __str__(self) -> str:
        return super().display_str()
    
    def reply(self, messages: list[str]) -> bool:
        curr_time = date.today()
        if self._last_message is not None:
            last_time = datetime.strptime(self._last_message, "%Y-%m-%d")
            if curr_time == last_time:
                messages['Ma mar kaptatok uzenetet', ' ', ' ', 'Peace out ( ´ ▽ ` )ﾉ']
        else:
            self._last_message = curr_time
        return super().reply(messages)
    
    def display_str(self) -> str:
        name = super().display_str()
        if self.unread:
            return f"👥 {name} 🔔"
        else:
            return f"👥 {name}"
    
    def archive(self):
        menu =  super().__archive()
        if len(menu) == 8:
            menu[4].click()
    
    def json_format(self) -> dict:
        return {"type" : "group", "last_message" : self._last_message, "keep_open" : self.keep_open, "name": self.name}