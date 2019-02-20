from flying_ioc import IocManager


class ClassA:
    pass


class ExampleClass:
    def __init__(self, value_text, value_class):
        assert value_text == 'Some text'
        assert value_class.__class__ == ClassA


def test_arguments():
    ioc = IocManager()
    ioc.set_value(name='value_text', value='Some text')
    ioc.set_value(name='value_class', value=ClassA())

    ioc.set_class(cls=ExampleClass)

    assert ioc.ExampleClass.__class__ == ExampleClass
