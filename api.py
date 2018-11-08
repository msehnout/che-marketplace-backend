from flask import Flask, Blueprint
from flask import jsonify
from flask_restful import Resource, Api
from werkzeug.contrib.cache import SimpleCache

from repo import Repository
from plugin import Plugin

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

repo = Repository()
cache = SimpleCache()


def get_cached_plugins(cache):
    plugins = cache.get('plugins')
    if plugins is None:
        plugins = repo.fetch_plugins_from_github()
        cache.set('plugins', plugins, timeout=600)
    return plugins


class AliveProbe(Resource):
    def get(self):
        return {'alive': 'yes'}


class PluginsList(Resource):
    def get(self):
        plugins = get_cached_plugins(cache)
        return jsonify(list(map(Plugin.as_dict, plugins)))


class SpecificPlugin(Resource):
    def get(self, name):
        plugins = get_cached_plugins(cache)
        return jsonify(next(p.as_dict() for p in plugins if p.name == name))


api.add_resource(AliveProbe, '/alive')
api.add_resource(PluginsList, '/plugins')
api.add_resource(SpecificPlugin, '/plugins/<string:name>')
app.register_blueprint(api_bp, url_prefix='/v1')

if __name__ == '__main__':
    app.run(debug=True)

