from somepackage.reloder import Reloder
from somepackage import anotherclass

class Test(Reloder):
    def __init__(self) -> None:
        ac = anotherclass.AnotherClass()
        ac.do_something()
        self.a = 3
        self.b = 2

    def calc(self):
        return 42