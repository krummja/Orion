from __future__ import annotations
import logging

import orion
from orion.plugins.scenes.scene import Scene

logger = logging.getLogger(__file__)


class SceneManager(orion.GamePlugin):

    def boot(self):
        pass

    def ready(self):
        pass

    def start(self):
        pass

    # Handler API

    def add(self, scene: Scene) -> None:
        pass

    def remove(self, scene: Scene) -> None:
        pass

    # Processor API

    def update(self, time: float, delta: float) -> None:
        pass

    def pre_render(self, time: float, delta: float) -> None:
        pass
