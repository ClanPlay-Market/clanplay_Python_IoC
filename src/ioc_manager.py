import traceback

from ioc_containers.class_container import ClassContainer
from ioc_containers.factory_container import FactoryContainer
from ioc_containers.singleton_container import SingletonContainer
from ioc_containers.value_container import ValueContainer


# phases:
# 1. only get by name, values, not creating classes
# 2. creating class, only singleton, no base classes
# 2a. singleton with args
# 3. only singleton, base class same or less arguments
# 4. only singleton, base class other arguments

class IocManager:
    def __init__(self, stats=False):
        self._containers = {}
        self._stats = {} if stats else None
        self.set_value('IocManager', self)

    def __getattr__(self, name):
        if name not in self._containers:
            raise AttributeError("Name '%s' does not exist" % name)
        try:
            return self._containers[name].get()
        except AttributeError as e:
            traceback.print_exception(e, e, e.__traceback__)
            raise RuntimeError(e)

    def set_value(self, name: str, value):
        self.__store_by_name(name, ValueContainer(value=value, stats=self._stats))

    def set_class(self, cls: type, name: str = None, singleton=False, thread_local=False):
        container = SingletonContainer if singleton else ClassContainer
        if name is None:
            name = cls.__name__
        self.__store_by_name(
            name,
            container(cls=cls, ioc_manager=self, stats=self._stats, thread_local=thread_local)
        )

    def set_factory(self, name: str, cls):
        self.__store_by_name(name, FactoryContainer(name=name, cls=cls, ioc_manager=self, stats=self._stats))

    def __store_by_name(self, name: str, value):
        if name in self._containers:
            raise AttributeError("Name '%s' is already defined" % name)
        self._containers[name] = value

    def print_stats(self):
        if self._stats:
            for key, value in self._stats.items():
                print('%s=%d' % (key, value))
