from ioc_decorator import NotInject
from ioc_manager import IocManager


class Parent1:
    def __init__(self):
        pass


class TSingleton1:
    # noinspection PyUnusedLocal
    def __init__(self, pr: Parent1, **kwargs):
        pass


@NotInject(['pr'])
class TSingleton2(TSingleton1):
    def __init__(self, **kwargs):
        pr = Parent1()
        super().__init__(pr, **kwargs)
        pass


@NotInject('a')
def example_func():
    pass


def test_singleton_args_diff2_container():
    print('TSingleton2=%s (%s)' % (TSingleton2.__name__, TSingleton2))
    print('example_func=%s (%s)' % (example_func.__name__, example_func))

    ioc = IocManager(stats=True)

    ioc.set_class(name='singleton2', cls=TSingleton2, singleton=True)
    ioc.set_class(name='Parent1', cls=Parent1, singleton=True)

    assert ioc.singleton2 is not None

    ioc.print_stats()
