# Inversion of control (IoC) for Humans - written in Python
[Inversion of control](https://en.wikipedia.org/wiki/Inversion_of_control)

## How to use it
pip install flying-ioc

``` {.sourceCode .python}
from flying_ioc import *

ioc = IocManager()

ioc.set_class(cls=HelperWrapper, singleton=True)
ioc.set_class(cls=GRHelperService, singleton=True)
ioc.set_class(name='api', cls=GRApiClient, singleton=True, thread_local=True)

gr_service: GRHelperService = ioc.GRHelperService
gr_service.start()
```

## Features
* Support getting an object as an attribute of IoC manager
* Initializing a class argument by the argument's class name and if not present by the argument name
* Support for inheritance - initializing arguments needed by parent classes
* Support mapping of values, classes, factories
* Support configuration of mapping like singleton, class per thread
* Support for @NotInject decorator

## Attribute
``` {.sourceCode .python}
gr_service: GRHelperService = ioc.GRHelperService
gr_service.start()
```
### Initializing a class
``` {.sourceCode .python}
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
```

## Support for inheritance
``` {.sourceCode .python}
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
```

## Values
``` {.sourceCode .python}
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
```

## Factory
``` {.sourceCode .python}
class ClassA:
    pass

class ClassB:
    pass

class ClassC:
    pass

class Factory(IocFactory):
    @staticmethod
    def get_instance(ioc_manager: IocManager, name: str, frame_info: inspect.FrameInfo):
        if frame_info.function == 'test_factory_1':
            return ioc_manager.ClassA

        if name == 'factory1':
            return ioc_manager.ClassB

        return ioc_manager.ClassC

ioc = IocManager()
ioc.set_class(cls=ClassA)
ioc.set_class(cls=ClassB)
ioc.set_class(cls=ClassC)
ioc.set_factory(name='factory1', cls=Factory)
ioc.set_factory(name='factory2', cls=Factory)

def test_factory_1():
    assert ioc.factory1.__class__ == ClassA
    assert ioc.factory2.__class__ == ClassA

def test_factory_2():
    assert ioc.factory1.__class__ == ClassB
    assert ioc.factory2.__class__ == ClassC
```
## Singleton
``` {.sourceCode .python}
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
```
## Class per thread
``` {.sourceCode .python}
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
```
## @NotInject decorator
In the following example, the @NotInject decorator prevents the IoC manager from adding arg1 to the kwargs argument when it initializes the ExampleClass, arg1 argument is needed by the parent class.

Removing the @NotInject decorator in this example will result in an exception.

The @NonInject decorator takes a list of argument names to skip in the initializing process.
``` {.sourceCode .python}
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
```
## Exceptions
IoC Manager raises two types of exceptions:
* AttributeError - when trying to get an undefined attribute from the IoC Manager
* TypeError - in the following cases:
  * IoC Manager is missing a container definition needed by the initialization of a
   class or it parent class 
  * While initializing a class, multiple instances of the same argument are provided 
  to it's parent class - by the user and also injected by IoC Manager. This issue 
  can be resolve using the @NotInject decorator 

``` {.sourceCode .python}
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

class ExampleClass2:
    def __init__(self, arg1: ClassC):
        pass

class ExampleClass3(ExampleClass2):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

ioc = IocManager()
ioc.set_class(cls=ClassA)
ioc.set_class(cls=ClassB)

def test_exception_container_not_defined():
    with pytest.raises(AttributeError) as e:
        ioc.NotExists
    assert e.value.args[0] == "Name 'NotExists' does not exist"

def test_exception_missing_not_inject():
    with pytest.raises(TypeError) as e:
        ioc.set_class(cls=ExampleClass1)
        ioc.ExampleClass1
    assert e.value.args[0] == "__init__() got multiple values for argument 'arg1'"

def test_exception_arg_is_not_defined():
    with pytest.raises(TypeError) as e:
        ioc.set_class(cls=ExampleClass2)
        ioc.ExampleClass2
    assert e.value.args[0].args[0] == "Can't get a container neither by class name ClassC, neither by arg name arg1"

def test_exception_arg_for_parent_is_not_defined():
    with pytest.raises(TypeError) as e:
        ioc.set_class(cls=ExampleClass3)
        ioc.ExampleClass3
    assert e.value.args[0] == "__init__() missing 1 required positional argument: 'arg1'"
```