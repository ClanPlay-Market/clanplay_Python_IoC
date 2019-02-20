class NotInject:
    _not_inject_classes = {}

    def __init__(self, containers):
        self._containers = containers

    def __call__(self, cls):
        self._not_inject_classes[cls] = self._containers
        return cls

    @staticmethod
    def get_not_injected_containers(cls: type):
        return NotInject._not_inject_classes.get(cls, [])
