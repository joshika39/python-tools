import sys
import importlib

class Reloder():
    def __init__(self) -> None:
        pass

    def reload(self):
        for module in list(sys.modules.values()):
            if "somepackage" in module.__name__:
                importlib.reload(module)