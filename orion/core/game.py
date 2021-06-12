from __future__ import annotations
from typing import Any, Dict, Optional

import logging
import pygame as pg

from orion.core.events import EventEmitter
from orion.core.config import OrionConfig
from orion.events import BOOT, POST_RENDER, POST_STEP, PRE_RENDER, PRE_STEP, READY, START, STEP, STOP, TEARDOWN
import orion._logging as log


logger = logging.getLogger(__file__)


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


class Game:

    def __init__(
            self,
            options: Optional[Dict[str, Any]] = None,
            config_path: Optional[str] = None,
        ) -> None:
        self.config = OrionConfig(options, config_path)
        self.loop = TimeStep(self)
        self.events = EventEmitter()

        self._is_booted = False
        self._is_running = False
        self._pending_teardown = False
        self._remove_display = False

        self.events.on(READY, self.start)

    def boot(self):
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
