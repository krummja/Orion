from __future__ import annotations
import logging

from orion.core.plugin import GamePlugin
from orion import events

logger = logging.getLogger(__file__)


class Renderer(GamePlugin):

    def boot(self):
        logger.info("BOOT: Renderer")

    def ready(self):
        logger.info("READY: Renderer")

    def start(self):
        logger.info("START: Renderer")
        self.root.events.on(events.PRE_ENDER, self.render)

    def pre_render(self, time: float, delta: float) -> None:
        print(delta)

    def render(self):
        pass

    def post_render(self):
        pass
