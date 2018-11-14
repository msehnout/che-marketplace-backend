import base64
import os
import yaml

from flask import current_app
from github import Github, GithubException
from che_marketplace_backend.plugin import Plugin

METADATA_FILENAME = 'meta.yaml'
# Name of the repository on Github
PLUGIN_REGISTRY = 'eclipse/che-plugin-registry'


class Repository():

    def __init__(self):
        self.plugins = []
        # This seems to be lazy, so it will pass regardless the content of the token
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
        try:
            text = base64.b64decode(metadata_file.content).decode('utf-8')
        except base64.binascii.Error:
            # The input string contains letters that does not belong to the b64 alphabet
            current_app.logger.error("could not decode b64 encoded file at path " + str(metadata_file))
            return None
        except UnicodeError:
            # Error while decoding the byte stream, not valid UTF-8
            current_app.logger.error("could not decode UTF-8 encoded content of file at path "
                          + str(metadata_file))
            return None
        dict = yaml.safe_load(text)
        return Plugin.from_dict(dict) if dict is not None else None

    def fetch_plugins_from_github(self):
        current_app.logger.info("Running fetch plugins from Github")
        try:
            plugins_dirs = self._fetch_plugin_dirs()
            latest_versions = map(lambda x: self._fetch_latest_version(x), plugins_dirs)
            ret = list(filter(lambda x: x is not None,
                           map(lambda x: self._fetch_metadata(x), latest_versions)))
        except GithubException:
            current_app.logger.exception("Unhandled exception in the code dealing with Github API:")
            return []

        return ret