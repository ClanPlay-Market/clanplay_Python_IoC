import inspect

from flying_ioc import IocManager, IocFactory


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
