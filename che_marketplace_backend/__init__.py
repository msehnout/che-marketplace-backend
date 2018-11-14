from flask import Flask, Blueprint, current_app
from flask import jsonify
from flask.logging import default_handler
from flask_restful import Resource, Api
from werkzeug.contrib.cache import SimpleCache

from che_marketplace_backend.repo import Repository
from che_marketplace_backend.plugin import Plugin

import logging
import os


def setup_logging(flask_app):
    """Perform the setup of logging for this application."""
    if not flask_app.debug:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
        log_level = os.environ.get('FLASK_LOGGING_LEVEL', logging.getLevelName(logging.WARNING))
        handler.setLevel(log_level)

        flask_app.logger.removeHandler(default_handler)
        flask_app.logger.addHandler(handler)
        flask_app.logger.setLevel(logging.DEBUG)


def create_app(test_config=None):
    app = Flask(__name__)
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    repo = Repository()
    cache = SimpleCache()

    setup_logging(app)

    def get_cached_plugins(cache):
        plugins = cache.get('plugins')
        if plugins is None:
            plugins = repo.fetch_plugins_from_github()
            cache.set('plugins', plugins, timeout=1800)
        return plugins

    class AliveProbe(Resource):
        def get(self):
            current_app.logger.debug("yes, I'm alive")
            return {'alive': 'yes'}

    class PluginsList(Resource):
        def get(self):
            plugins = get_cached_plugins(cache)
            return jsonify(list(map(Plugin.as_dict, plugins)))

    class SpecificPlugin(Resource):
        def get(self, id):
            plugins = get_cached_plugins(cache)
            try:
                pkg = next(p.as_dict() for p in plugins if p.id == id)
            except StopIteration:
                current_app.logger.info("request for unknown package: " + id)
                return {'error': 'package does not exist'}

            return jsonify(pkg)

    api.add_resource(AliveProbe, '/alive')
    api.add_resource(PluginsList, '/plugins')
    api.add_resource(SpecificPlugin, '/plugins/<string:id>')
    app.register_blueprint(api_bp, url_prefix='/v1')

    return app


