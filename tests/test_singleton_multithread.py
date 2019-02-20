import threading

from flying_ioc import IocManager


class TSingleton1:
    def __init__(self):
        pass


def _set_vars(ioc: IocManager, storage: dict):
    def wrapped():
        storage['singleton1'] = ioc.singleton1
        storage['singleton2'] = ioc.singleton2

    return wrapped


def test_multithread():
    ioc = IocManager(stats=True)

    ioc.set_class(name='singleton1', cls=TSingleton1, singleton=True)
    ioc.set_class(name='singleton2', cls=TSingleton1, singleton=True, thread_local=True)

    assert ioc.singleton1 is ioc.singleton1
    assert ioc.singleton2 is ioc.singleton2

    storage = {}
    thread = threading.Thread(target=_set_vars(ioc, storage))
    thread.start()
    thread.join()

    assert ioc.singleton1 is storage['singleton1']
    assert ioc.singleton2 is not storage['singleton2']

