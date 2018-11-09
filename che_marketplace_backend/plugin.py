# Data classes FTW, use latest-greatest!


class Plugin():
    def __init__(self):
        self.id = None
        self.version = None
        self.type = None
        self.name = None
        self.title = None
        self.description = None
        self.icon = None
        self.url = None

    @staticmethod
    def from_dict(dict):
        new_plugin = Plugin()
        for attribute, value in dict.items():
            setattr(new_plugin, attribute, value)

        return new_plugin

    def as_dict(self):
        return self.__dict__


text = """id: che-dummy-plugin
version: 0.0.1
type: Che Plugin
name: Che Samples Hello World Plugin
title: Che Samples Hello World Plugin
description: A hello world theia plug-in wrapped into a Che Plug-in
icon: https://www.eclipse.org/che/images/ico/16x16.png
url: https://github.com/ws-skeleton/che-dummy-plugin/releases/download/untagged-8f3e198285a2f3b6b2db/che-dummy-plugin.tar.gz
"""

if __name__ == "__main__":
    import yaml
    plugin = Plugin.from_dict(yaml.load(text))
    print(plugin)
