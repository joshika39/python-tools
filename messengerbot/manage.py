from selection_picker_joshika39 import FunctionItem, SingleMenu, MenuWrapper
from jsonlib.json_service import JsonService
from botlib.base import proj_root
from conversations.conversation import Conversation
from conversations.factory import ConversationFactory
import os

testers_path = os.path.join(proj_root(), '../lists.json')
service = JsonService(testers_path)


fact = ConversationFactory(JsonService(os.path.join(
    proj_root(), '../users.json')), "https://google.com/")

conversations = fact.create_conversations(None)


def add_beta():
    testers = service.read("beta_testers")  # type: list
    selected = SingleMenu("Select the new tester",
                          [c for c in conversations if c.id not in testers]
                          ).show()  # type: Conversation
    if selected is not None:
        testers.append(selected.id)
        service.write("beta_testers", testers)


def remove_beta():
    testers = service.read("beta_testers")  # type: list
    tester_c = fact.create_conversations_from_list(None, testers)
    selected = SingleMenu("Select the new tester",
                          [c for c in tester_c if c.id]
                          ).show()  # type: Conversation

    if selected is not None:
        testers.remove(selected.id)
        service.write("beta_testers", testers)


MenuWrapper("Select an operation", [
    FunctionItem("Add new tester", add_beta),
    FunctionItem("Remove tester", remove_beta)
]).show()
