from ioc_containers.class_container import ClassContainer


class SingletonContainer(ClassContainer):
    def __init__(self, cls, ioc_manager, stats=None, thread_local=False):
        super().__init__(cls=cls, ioc_manager=ioc_manager, stats=stats, thread_local=thread_local)

    def get(self):
        instance = getattr(self._instance, 'value', None)
        if instance is not None:
            self._report_stats_action('get')
            return instance

        self._instance.value = super().get()
        self._report_stats_action('store')
        return self._instance.value
