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

    def __init__(self, root):
        self.root = root

    def _boot(self):
        print("Bar!")


class TestGame(orion.Game):
    pass


class Renderer(orion.GamePlugin):

    def boot(self):
        pass

    def ready(self):
        pass

    def start(self):
        self.root.events.on(orion.events.PRE_RENDER, self.pre_render)

    def pre_render(self, time: float, delta: float) -> None:
        print(delta)

    def render(self, time: float, delta: float):
        pass

    def post_render(self):
        pass


if __name__ == '__main__':
    manager = orion.OrionManager(TestGame)
    manager.boot()
