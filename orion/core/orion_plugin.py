from orion.core.registry import OrionPluginRegistry
from orion.events import BOOT, READY, START


class OrionPlugin(metaclass= OrionPluginRegistry):
    """Base class for registering plugins to the Orion framework.

    All OrionPlugins come equipped with an EventEmitter to handle
    inter-plugin communications.
    """

    def _boot(self):
        self.boot()
        self.events.emit(BOOT, str(self.__class__.__name__))

    def _ready(self):
        self.ready()
        self.events.emit(READY, str(self.__class__.__name__))

    def _start(self):
        self.start()
        self.events.emit(START, str(self.__class__.__name__))

    def boot(self):
        raise NotImplementedError

    def ready(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError
