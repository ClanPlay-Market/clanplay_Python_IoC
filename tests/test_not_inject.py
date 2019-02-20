from flying_ioc import IocManager, NotInject


class ClassA:
    pass


class ClassB:
    pass


class Parent:
    def __init__(self, arg1: ClassA, **kwargs):
        super().__init__(**kwargs)
        self._arg1 = arg1


@NotInject(['arg1'])
class ExampleClass(Parent):
    def __init__(self, arg2: ClassB, **kwargs):
        arg1 = ClassA()
        super().__init__(arg1, **kwargs)
        assert self._arg1 == arg1
        assert arg2.__class__ == ClassB


def test_not_inject():
    ioc = IocManager()
    ioc.set_class(cls=ClassA)
    ioc.set_class(cls=ClassB)

    ioc.set_class(cls=ExampleClass)

    assert ioc.ExampleClass.__class__ == ExampleClass
