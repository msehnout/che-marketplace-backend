# Data classes FTW, use latest-greatest!
from typing import Dict, Type, TypeVar

T = TypeVar('T', bound='Plugin')


class Plugin():
    def __init__(self):
        self.id: str = None             # Well defined string? e.g. [[:alpha:]]+[-_[:alpha:]]+
        self.version: str = None        # We need sth with defined ordering: e.g. semver!
        self.type: str = None
        self.name: str = None
        self.title: str = None
        self.description: str = None
        self.icon: str = None
        self.url: str = None

    @staticmethod
    def from_dict(dict: Dict[str, str]) -> T:
        new_plugin = Plugin()
        for attribute, value in dict.items():
            setattr(new_plugin, attribute, value)

        return new_plugin

    def as_dict(self) -> Dict[str, str]:
        return self.__dict__
