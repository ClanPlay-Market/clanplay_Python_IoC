from ioc_containers.base_container import BaseContainer


class ValueContainer(BaseContainer):
    def __init__(self, value, stats):
        super().__init__(storage=value, stats=stats)
        self._report_stats_action('store')

    def get(self):
        self._report_stats_action('get')
        return self._storage
