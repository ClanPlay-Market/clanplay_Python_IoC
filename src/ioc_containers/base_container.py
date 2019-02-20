from abc import ABC, abstractmethod


class BaseContainer(ABC):

    def __init__(self, storage, stats=None):
        self._storage = storage
        self._stats = stats

    @abstractmethod
    def get(self):
        raise NotImplementedError()

    def _report_stats_action(self, action_name, counter=1):
        if self._stats is None:
            return

        name = '%s_%s' % (self.__class__.__name__, action_name)

        if name not in self._stats:
            self._stats[name] = 0

        self._stats[name] += counter
