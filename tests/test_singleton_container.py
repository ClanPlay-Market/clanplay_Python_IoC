from ioc_manager import IocManager


class TSingleton1:
    def __init__(self):
        pass


def test_singleton_container():
    ioc = IocManager(stats=True)

    ioc.set_class(name='singleton1', cls=TSingleton1, singleton=True)

    assert ioc.singleton1 is ioc.singleton1

    ioc.print_stats()
