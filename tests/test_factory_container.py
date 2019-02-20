from ioc_containers.factory_container import Factory
from ioc_manager import IocManager


class TSingleton1:
    def __init__(self):
        pass


class TSingleton2:
    def __init__(self):
        pass


class TSingleton3(TSingleton1):
    def __init__(self, ts: TSingleton2):
        super().__init__()
        self.ts = ts


class TSingleton3dot2(TSingleton3):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TSingleton3dot1(TSingleton3):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TSingleton3dot3:
    def __init__(self, ts: TSingleton2):
        self.ts = ts


class MyFactory(Factory):
    @staticmethod
    def get_instance(ioc_manager, name, frame_info):
        if frame_info.function == 'test_factory_container':
            return ioc_manager.TSingleton3dot1

        if name == 'TSingleton3':
            return ioc_manager.TSingleton3dot2

        return ioc_manager.TSingleton3dot3


def test_factory_container():
    ioc = IocManager(stats=True)

    ioc.set_class(name='TSingleton1', cls=TSingleton1, singleton=True)
    ioc.set_class(name='TSingleton2', cls=TSingleton2, singleton=False)
    ioc.set_factory(name='TSingleton3', cls=MyFactory)
    ioc.set_class(name='TSingleton3dot1', cls=TSingleton3dot1, singleton=False)
    ioc.set_class(name='TSingleton3dot2', cls=TSingleton3dot2, singleton=False)
    ioc.set_class(name='TSingleton3dot3', cls=TSingleton3dot3, singleton=False)

    assert ioc.TSingleton1 is ioc.TSingleton1
    ts3 = ioc.TSingleton3
    assert isinstance(ts3, TSingleton3dot1)

    ioc.print_stats()
