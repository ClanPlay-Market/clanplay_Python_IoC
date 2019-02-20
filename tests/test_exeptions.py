import pytest

from flying_ioc import IocManager


class ClassA:
    pass


class ClassB:
    pass


class ClassC:
    pass


class Parent:
    def __init__(self, arg1: ClassA, **kwargs):
        super().__init__(**kwargs)
        self._arg1 = arg1


class ExampleClass1(Parent):
    def __init__(self, arg2: ClassB, **kwargs):
        arg1 = ClassA()
        super().__init__(arg1, **kwargs)
        assert self._arg1 == arg1
        assert arg2.__class__ == ClassB


# noinspection PyUnusedLocal
class ExampleClass2:
    def __init__(self, arg1: ClassC):
        pass


# noinspection PyUnusedLocal
class ExampleClass3(ExampleClass2):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


ioc = IocManager()
ioc.set_class(cls=ClassA)
ioc.set_class(cls=ClassB)


# noinspection PyStatementEffect
def test_exception_container_not_defined():
    with pytest.raises(AttributeError) as e:
        ioc.NotExists
    assert e.value.args[0] == "Name 'NotExists' does not exist"


# noinspection PyStatementEffect
def test_exception_missing_not_inject():
    with pytest.raises(TypeError) as e:
        ioc.set_class(cls=ExampleClass1)
        ioc.ExampleClass1
    assert e.value.args[0] == "__init__() got multiple values for argument 'arg1'"


# noinspection PyStatementEffect
def test_exception_arg_is_not_defined():
    with pytest.raises(TypeError) as e:
        ioc.set_class(cls=ExampleClass2)
        ioc.ExampleClass2
    assert e.value.args[0].args[0] == "Can't get a container neither by class name ClassC, neither by arg name arg1"


# noinspection PyStatementEffect
def test_exception_arg_for_parent_is_not_defined():
    with pytest.raises(TypeError) as e:
        ioc.set_class(cls=ExampleClass3)
        ioc.ExampleClass3
    assert e.value.args[0] == "__init__() missing 1 required positional argument: 'arg1'"
