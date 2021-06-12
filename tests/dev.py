from __future__ import annotations

import orion
import dev2


class TestPlugin(orion.GamePlugin):

    def boot(self):
        print("Foo!")

    def ready(self):
        pass

    def start(self):
        pass


class TestPlugin2(orion.OrionPlugin):

    def _boot(self):
        print("Bar!")


class TestGame(orion.Game):
    pass


if __name__ == '__main__':
    manager = orion.OrionManager(TestGame)
    manager.boot()
