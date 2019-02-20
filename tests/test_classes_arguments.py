from flying_ioc import IocManager


class ClassA:
    pass


class ClassB:
    pass


class ClassC:
    pass


class ExampleClass:
    def __init__(self, arg1: ClassA, arg2, arg3: ClassC):
        assert arg1.__class__ == ClassA
        assert arg2.__class__ == ClassB
        assert arg3.__class__ == ClassC


def test_arguments():
    ioc = IocManager()
    ioc.set_class(cls=ClassA)
    ioc.set_class(name='arg2', cls=ClassB)
    ioc.set_class(name='arg3', cls=ClassC)

    ioc.set_class(cls=ExampleClass)

    assert ioc.ExampleClass.__class__ == ExampleClass
