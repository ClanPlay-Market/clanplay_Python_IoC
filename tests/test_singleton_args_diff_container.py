from flying_ioc import IocManager


class Parent1:
    def __init__(self):
        pass


class TSingleton1:
    # noinspection PyUnusedLocal
    def __init__(self, pr: Parent1):
        pass


class TSingleton2(TSingleton1):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


def test_singleton_args_diff_container():
    ioc = IocManager(stats=True)

    ioc.set_class(name='singleton2', cls=TSingleton2, singleton=True)
    ioc.set_class(name='Parent1', cls=Parent1, singleton=True)

    assert ioc.singleton2 is not None

    ioc.print_stats()
