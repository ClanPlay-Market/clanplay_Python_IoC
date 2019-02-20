from typing import List


class NotInject:
    _not_inject_classes = {}

    def __init__(self, names: List[str]):
        self._names = names

    def __call__(self, cls):
        self._not_inject_classes[cls] = self._names
        return cls

    @staticmethod
    def get_not_injected_names(cls: type):
        return NotInject._not_inject_classes.get(cls, [])
