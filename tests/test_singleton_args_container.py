from ioc_manager import IocManager


class TSingleton1:
    def __init__(self):
        pass


class TSingleton2:
    def __init__(self, ts: TSingleton1):
        self.ts = ts
        pass


def test_singleton_args_container():
    stats = {}
    ioc = IocManager(stats)

    ioc.set_class(name='TSingleton1', cls=TSingleton1, singleton=True)
    ioc.set_class(name='singleton2', cls=TSingleton2, singleton=True)

    assert ioc.singleton2 is ioc.singleton2

    assert ioc.TSingleton1 is ioc.TSingleton1

    assert ioc.singleton2.ts is ioc.TSingleton1

    ioc.print_stats()
