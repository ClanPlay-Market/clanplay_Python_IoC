from flying_ioc import IocManager


class ClassA:
    pass


class ClassB:
    pass


def test_singleton():
    ioc = IocManager()
    ioc.set_class(cls=ClassA)
    ioc.set_class(cls=ClassB, singleton=True)

    assert ioc.ClassA != ioc.ClassA
    assert ioc.ClassB == ioc.ClassB
