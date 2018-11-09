import base64
import os
import yaml

from github import Github
from che_marketplace_backend.plugin import Plugin

METADATA_FILENAME = 'meta.yaml'
# Name of the repository on Github
PLUGIN_REGISTRY = 'eclipse/che-plugin-registry'


class Repository():
    def __init__(self):
        self.plugins = []
        self.g = Github(os.environ['CHE_PLUGIN_DEV_TOKEN'])
        self.repo = None

    def _fetch_plugin_dirs(self):
        self.repo = self.g.get_repo(PLUGIN_REGISTRY)
        plugins_unfiltered = self.repo.get_contents("plugins")
        plugins_dirs = filter(lambda x: x.type == "dir", plugins_unfiltered)
        return plugins_dirs

    def _fetch_latest_version(self, dir):
        versions = self.repo.get_contents(dir.path)
        # TODO: sort and get the latest (but there is no plugin with multiple versions, so currently
        # TODO: I don't know how to sort it), also we need some versioning strategy (like semver)
        return versions[0]

    def _fetch_metadata(self, plugin_path):
        metadata_file = self.repo.get_contents(plugin_path.path + '/' + METADATA_FILENAME)
        text = base64.b64decode(metadata_file.content).decode('utf-8')
        dict = yaml.safe_load(text)
        return Plugin.from_dict(dict) if dict is not None else None

    def fetch_plugins_from_github(self):
        plugins_dirs = self._fetch_plugin_dirs()
        latest_versions = map(lambda x: self._fetch_latest_version(x), plugins_dirs)
        return list(filter(lambda x: x is not None,
                           map(lambda x: self._fetch_metadata(x), latest_versions)))


if __name__ == '__main__':
     r = Repository()
     pl = r.fetch_plugins_from_github()
     for p in pl:
         print(p.name + " " + p.version)