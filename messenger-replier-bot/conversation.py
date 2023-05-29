from json_service import JsonService

class Conversation():
    def __init__(self, service: JsonService, id) -> None:
        self.service = service
        self.id = id
        self.type = self.service.read(f"{id}/type")
        self.last_message = self.service.read(f"{id}/last_message")

    # def reply(self):
    #     self.last_message = 