import threading

from flying_ioc import IocManager


class ClassA:
        pass


def _set_vars(ioc: IocManager, storage: dict):
    def wrapped():
        storage['singleton1'] = ioc.singleton1
        storage['singleton2'] = ioc.singleton2

    return wrapped


def test_class_per_thread():
    ioc = IocManager()

    ioc.set_class(name='singleton1', cls=ClassA, singleton=True)
    ioc.set_class(name='singleton2', cls=ClassA, singleton=True, thread_local=True)

    assert ioc.singleton1 == ioc.singleton1
    assert ioc.singleton2 == ioc.singleton2

    thread_storage = {}
    thread = threading.Thread(target=_set_vars(ioc, thread_storage))
    thread.start()
    thread.join()

    assert ioc.singleton1 == thread_storage['singleton1']
    assert ioc.singleton2 != thread_storage['singleton2']

