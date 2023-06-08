from conversations.imports import *

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

    def json_format(self) -> dict:
        pass

    def save(self):
        json_obj = self.json_format()
        self.service.write(f"conversations/{self.id}", json_obj)