from orion import OrionPlugin, GamePlugin
from typing import Optional


class OtherPlugin(OrionPlugin):
    pass


class AnotherPlugin(GamePlugin):

    def boot(self):
        pass

    def ready(self):
        pass

    def start(self):
        pass
