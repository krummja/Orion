from __future__ import annotations

from abc import ABCMeta
from typing import Mapping, List, TYPE_CHECKING, AbstractSet

if TYPE_CHECKING:
    from orion.core.orion_plugin import OrionPlugin


class OrionPluginRegistry(Mapping, metaclass=ABCMeta):

    def __contains__(self, key: str) -> bool:
        pass

    def __dir__(self) -> List[str]:
        return list(self.keys())

    def __getitem__(self, key: str) -> OrionPlugin:
        pass

    def __iter__(self) -> AbstractSet[str]:
        return self.keys()
