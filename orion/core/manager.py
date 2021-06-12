from __future__ import annotations
from typing import Type, Optional, AbstractSet, Iterable, Hashable, ItemsView, TypeVar
import logging
import inspect
import functools

from orion.events import *
from orion.core.game import Game
from orion.core.plugin import OrionPlugin, GamePlugin
from orion.core.registry import OrionPluginRegistry, T

logger = logging.getLogger(__file__)


def partial_class(cls, *args, **kwargs):

    class NewCls(cls):
        __init__ = functools.partialmethod(cls.__init__, *args, **kwargs)
    return NewCls


class OrionManager:
    BOOTED = {}

    def __init__(self, root: Optional[Type[Game]] = None) -> None:
        if root:
            self._root = root()
            if not isinstance(self._root, Game):
                raise RuntimeWarning("Expected root to be of type orion.Game. Did you inherit from orion.Game?")
        else:
            self._root = Game()

    @property
    def root(self) -> Game:
        return self._root

    @property
    def registry(self):
        return OrionPluginRegistry

    def __iter__(self):
        return iter(self.registry.REGISTRY.keys())

    def __len__(self) -> int:
        return len(self.registry.REGISTRY)

    def __getitem__(self, key: str) -> Type[T]:
        return self.registry.get_class(key)

    def get(self, key: str) -> Type[T]:
        """Get an uninitialized plugin class from the registry."""
        class_type: Type[T] = self[key]
        return class_type

    def new(self, key: str) -> T:
        """Instantiate a class from the plugin registry."""
        plugin_instance: T = self.registry.get(key)
        return plugin_instance

    def boot(self):
        for plugin in self.registry.REGISTRY.values():
            if plugin.__name__ == "GamePlugin":
                continue
            if hasattr(plugin, "_boot"):
                _plugin = plugin()
                if hasattr(plugin, "is_booted"):
                    _plugin.is_booted = True
                else:
                    setattr(_plugin, "is_booted", True)

                self.root.events.on(BOOT, _plugin._boot)

                if hasattr(plugin, "_ready"):
                    self.root.events.on(READY, _plugin._ready)

                if hasattr(plugin, "_start"):
                    self.root.events.on(START, _plugin._start)

                self.BOOTED[_plugin.__class__.__name__] = _plugin

        self.root.boot()

        if all([plugin.is_booted for plugin in self.BOOTED.values()]):
            self.root.ready()
