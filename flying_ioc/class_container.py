import inspect
import threading

from flying_ioc.base_container import BaseContainer
from flying_ioc import NotInject


class ClassContainer(BaseContainer):
    def __init__(self, cls, ioc_manager, stats=None, thread_local=False):
        super().__init__(storage=cls, stats=stats)
        self._ioc_manager = ioc_manager
        self._instance = threading.local() if thread_local else self

    def get(self):
        init_args = getattr(self._instance, 'init_args', None)
        if init_args is not None:
            return self.__create_class_instance(init_args)

        init_args = {}

        not_inject = NotInject.get_not_injected_names(self._storage)
        args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = \
            self.__fill_args(self._storage, init_args, not_inject=not_inject)

        # if **kwargs is a param in the constructor
        if kwonlyargs is not None:
            self.__fill_base_classes_args(self._storage, init_args, not_inject)

        ret_val = self.__create_class_instance(init_args)
        self._instance.init_args = init_args
        return ret_val

    def __fill_args(self, cls, init_args, not_inject, raise_error=True):
        args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(cls)

        for arg in args:
            if arg == 'self':
                continue

            if arg in init_args:
                continue

            if arg in not_inject:
                continue

            arg_class = annotations.get(arg)

            if arg_class is not None:
                if arg_class.__name__ in not_inject:
                    continue
                try:
                    value = getattr(self._ioc_manager, arg_class.__name__)
                    init_args[arg] = value
                    continue
                except AttributeError:
                    pass

            try:
                value = getattr(self._ioc_manager, arg)
                init_args[arg] = value
            except AttributeError:
                if raise_error:
                    raise AttributeError("Can't get a container neither by class name %s, neither by arg name %s"
                                         % (arg_class.__name__, arg))

        return args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations

    def __fill_base_classes_args(self, cls, init_args, not_inject):
        for c in cls.__bases__:
            args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = \
                self.__fill_args(c, init_args, not_inject=not_inject, raise_error=False)

            if kwonlyargs is not None:
                self.__fill_base_classes_args(c, init_args, not_inject=not_inject)

    def __create_class_instance(self, init_args):
        try:
            ret_val = self._storage(**init_args)
        except TypeError as e:
            print('TypeError when constructing %s: %s' % (self._storage.__name__, e.args))
            print('%s(%s)' % (self._storage.__name__,
                              ', '.join(['%s=%s' % (key, value) for key, value in init_args.items()])
                              ))
            raise e
        self._report_stats_action('create_instance')
        self._report_stats_action('get')
        return ret_val
