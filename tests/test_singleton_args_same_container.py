from ioc_manager import IocManager


class Parent0:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Parent1(Parent0):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TSingleton1(Parent1):
    # noinspection PyUnusedLocal
    def __init__(self, pr: Parent1, **kwargs):
        super().__init__(**kwargs)


class TSingleton2(TSingleton1):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def test_singleton_args_same_container():
    ioc = IocManager(stats=True)

    ioc.set_class(name='singleton2', cls=TSingleton2, singleton=True)
    ioc.set_class(name='Parent1', cls=Parent1, singleton=True)

    assert ioc.singleton2 is not None

    ioc.print_stats()
