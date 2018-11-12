from che_marketplace_backend.plugin import Plugin

dic = {
        'description':'A test project',
        'title': 'A test plugin',
        'url': 'https://test.plugin.com',
        'name': 'che test plugin',
        'version': '0.0.1',
        'type': 'test plugin',
        'id': 'che test',
        'icon': 'https://test.che.plugin/icon.png'
    }


def test_from_dict():
    plugin = Plugin()
    obj = plugin.from_dict(dic)
    assert obj.description == 'A test project'
    assert obj.title == 'A test plugin'
    assert obj.url == 'https://test.plugin.com'
    assert obj.name == 'che test plugin'
    assert obj.version == '0.0.1'
    assert obj.type == 'test plugin'
    assert obj.id == 'che test'
    assert obj.icon == 'https://test.che.plugin/icon.png'


def test_as_dict():
    plugin = Plugin()
    res = plugin.as_dict()
    assert res == {
        'description': None,
        'title': None,
        'url': None,
        'name': None,
        'version': None,
        'type': None,
        'id': None,
        'icon': None
    }
    assert type(res) == dict
