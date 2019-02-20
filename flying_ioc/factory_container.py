import inspect
from abc import ABC, abstractmethod

from flying_ioc.base_container import BaseContainer


class IocFactory(ABC):
    @staticmethod
    @abstractmethod
    def get_instance(ioc_manager, name: str, frame_info: inspect.FrameInfo):
        raise NotImplementedError()


class FactoryContainer(BaseContainer):

    def get(self):
        stack = inspect.stack()
        i = 0
        while i < len(stack):
            slf = stack[i].frame.f_locals.get('self')
            i += 1
            if slf and slf.__class__.__name__ == 'IocManager':
                break

        frame_info = stack[i]
        return self._storage.get_instance(ioc_manager=self._ioc_manager, name=self._name, frame_info=frame_info)

    def __init__(self, name, cls, ioc_manager, stats=None):
        if not issubclass(cls, IocFactory):
            raise AttributeError('Argument cls should be a subclass of Factory')
        super().__init__(storage=cls, stats=stats)
        self._ioc_manager = ioc_manager
        self._name = name
