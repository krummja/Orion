from __future__ import annotations
from typing import Type, Optional
import logging

from orion.events import *
from orion.core.orion_plugin import OrionPlugin
from orion.core.registry import OrionPluginRegistry

logger = logging.getLogger(__file__)


class OrionManager:

    def __init__(self, root: Optional[Type[OrionPlugin]] = None) -> None:
        self._root = root


# class OrionManager:
#
#     def __init__(self, root: Optional[Type[OrionPlugin]] = None) -> None:
#         self.root = root
#         self.boot_status = {}
#
#         for key, plugin in OrionPluginRegistry.plugins().items():
#             if key == "OrionPlugin":
#                 continue
#             self.boot_status[key] = False
#             self.boot_plugin(plugin)
#
#         for key in OrionPluginRegistry.plugins().keys():
#             if key == "OrionPlugin":
#                 continue
#             plugin = OrionPluginRegistry.get(key)
#             plugin.events.on(BOOT, self._set_ready)
#
#         if self.root:
#             self.root.events.on(READY, self.root.start)
#
#     def boot_plugin(self, plugin: Type[OrionPlugin]) -> OrionPlugin:
#         _plugin = plugin()
#         OrionPluginRegistry.add_booted(_plugin)
#         if self.root:
#             self.root.events.on(BOOT, _plugin._boot)
#             self.root.events.on(READY, _plugin._ready)
#             self.root.events.on(START, _plugin._start)
#         return _plugin
#
#     def _set_ready(self, key: str) -> None:
#         self.boot_status[key] = True
#         if all([value is True for value in self.boot_status.values()]):
#             self.root.ready()
