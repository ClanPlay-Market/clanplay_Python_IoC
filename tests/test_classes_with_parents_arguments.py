from flying_ioc import IocManager


class ClassA:
    pass


class ClassB:
    pass


class ClassC:
    pass


class ParentD:
    def __init__(self, arg1: ClassA, **kwargs):
        self._arg1 = arg1


class ParentE(ParentD):
    def __init__(self, arg2: ClassB, **kwargs):
        super().__init__(**kwargs)
        self._arg2 = arg2


class ExampleClass(ParentE):
    def __init__(self, arg3: ClassC, **kwargs):
        super().__init__(**kwargs)
        assert self._arg1.__class__ == ClassA
        assert self._arg2.__class__ == ClassB
        assert arg3.__class__ == ClassC


def test_arguments():
    ioc = IocManager()
    ioc.set_class(cls=ClassA)
    ioc.set_class(cls=ClassB)
    ioc.set_class(cls=ClassC)

    ioc.set_class(cls=ExampleClass)

    assert ioc.ExampleClass.__class__ == ExampleClass
