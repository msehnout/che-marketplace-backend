from flask import Flask, Blueprint
from flask import jsonify
from flask_restful import Resource, Api
from werkzeug.contrib.cache import SimpleCache

from che_marketplace_backend.repo import Repository
from che_marketplace_backend.plugin import Plugin


def create_app(test_config=None):
    app = Flask(__name__)
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    repo = Repository()
    cache = SimpleCache()


    def get_cached_plugins(cache):
        plugins = cache.get('plugins')
        if plugins is None:
            plugins = repo.fetch_plugins_from_github()
            cache.set('plugins', plugins, timeout=1800)
        return plugins


    class AliveProbe(Resource):
        def get(self):
            return {'alive': 'yes'}


    class PluginsList(Resource):
        def get(self):
            plugins = get_cached_plugins(cache)
            return jsonify(list(map(Plugin.as_dict, plugins)))


    class SpecificPlugin(Resource):
        def get(self, id):
            plugins = get_cached_plugins(cache)
            return jsonify(next(p.as_dict() for p in plugins if p.id == id))


    api.add_resource(AliveProbe, '/alive')
    api.add_resource(PluginsList, '/plugins')
    api.add_resource(SpecificPlugin, '/plugins/<string:id>')
    app.register_blueprint(api_bp, url_prefix='/v1')

    return app


