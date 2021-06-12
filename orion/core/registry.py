from __future__ import annotations

from typing import Mapping, List, TYPE_CHECKING, TypeVar, Type

from orion.core.events import EventEmitter
from orion.core.game import Game

if TYPE_CHECKING:
    from orion.core.plugin import OrionPlugin


T = TypeVar("T")


class RegistryKeyError(KeyError):
    pass


class OrionPluginRegistry(type):
    REGISTRY = {}

    def __new__(mcs, name, bases, attrs):
        clsobj = type.__new__(mcs, name, bases, attrs)
        mcs.REGISTRY[clsobj.__name__] = clsobj
        clsobj.events = EventEmitter()
        return clsobj

    def __getitem__(self, key: str) -> OrionPlugin:
        return self.get(key)

    def __missing__(cls, key: str):
        raise RegistryKeyError(key)

    @classmethod
    def get(mcs, key: str, *args, **kwargs) -> T:
        class_: Type[T] = mcs.REGISTRY[key]
        return class_(*args, **kwargs)

    @classmethod
    def get_class(mcs, key: str) -> Type[T]:
        return mcs.REGISTRY[key]
