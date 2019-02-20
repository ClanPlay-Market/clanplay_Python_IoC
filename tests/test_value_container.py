from ioc_manager import IocManager


def test_value_container():
    ioc = IocManager(stats=True)

    config_value = 'config_value'
    ioc.set_value('config', config_value)
    ioc.set_value('config1', config_value)
    ioc.set_value('config2', config_value)

    assert ioc.config is ioc.config1
    assert ioc.config1 is ioc.config2

    ioc.print_stats()
