from typing import Any, Dict, Optional

from orion.core.config import OrionConfig
from orion.core.manager import logger
from orion.core.orion_plugin import OrionPlugin
from orion.core.registry import OrionPluginRegistry
from orion.events import BOOT, POST_RENDER, POST_STEP, PRE_RENDER, PRE_STEP, READY, START, STEP, STOP, TEARDOWN


class TimeStep:

    def __init__(self, game: Game) -> None:
        log.configure(game.config)
        self.game = game

        self.clock = pg.time.Clock()
        self.runtime = 0
        self.frame = 0
        self.ticks = 0

        self._callback = None
        self._started = False
        self._is_running = False
        self._start_time = 0
        self._last_time = 0
        self._now = 0

    def start(self, callback) -> None:
        if self._started:
            return

        self._callback = callback
        self._started = True
        self._is_running = True
        self._start_time = self.clock.get_time()

        while self._is_running:
            self.step()

    def step(self):
        self._now = time = self.clock.get_time()
        dt = time - self._last_time

        self.runtime += dt
        self._callback(time, dt)
        self.clock.tick()

        self._last_time = time
        self.ticks += 1
        self.frame += 1

    def stop(self):
        self._is_running = False
        self._started = False
        self.teardown()

    def teardown(self):
        self._callback = None
        self.game = None

    def tick(self):
        self.tick()


class Game(OrionPlugin):

    def __init__(
            self,
            options: Optional[Dict[str, Any]] = None,
            config_path: Optional[str] = None,
        ) -> None:
        """The core client object that serves as the central interface
        with the rest of the framework.

        Different packages that provide certain kinds of functionality
        can be dropped into this basic class like plugins.

        Access plugins using the `OrionPluginRegistry.plugins()` classmethod.
        Register them by extending the `OrionPlugin` class.

        Access plugins by key using the registry's `get_plugin` method, e.g.
            plugin = OrionPluginRegistry.get_plugin("MyPlugin")
        """
        self.config = OrionConfig(options, config_path)
        self.loop = TimeStep(self)

        self._is_booted = False
        self._is_running = False
        self._pending_teardown = False
        self._remove_display = False

    def boot(self):
        OrionPluginRegistry.add_booted(self)
        logger.info("BOOT")
        self._is_booted = True
        self.events.emit(BOOT)

    def ready(self):
        logger.info("READY")
        self.events.emit(READY)

    def start(self):
        logger.info("All Orion Plugins report READY status. Starting main loop.")
        self.events.emit(START)

        self.events.on(STOP, self.stop)
        self._is_running = True
        self.loop.start(self.step)

    def step(self, time: float, delta: float):
        if self._pending_teardown:
            self.teardown()

        emitter = self.events

        emitter.emit(PRE_STEP, time, delta)
        emitter.emit(STEP, time, delta)
        emitter.emit(POST_STEP, time, delta)
        emitter.emit(PRE_RENDER, time, delta)
        emitter.emit(POST_RENDER, time, delta)

    def stop(self):
        self._is_running = False
        self._pending_teardown = True
        self.events.emit(TEARDOWN)

    def teardown(self):
        pass
