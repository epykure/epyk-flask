from flask import Flask, Blueprint
import importlib
from epyk_flask import epyk_engine
app = Flask(__name__)



def init_flask_app():
  for endpoint in epyk_engine.config['endpoints']['blueprints']:
    mod = importlib.import_module(endpoint)
    app.register_blueprint(getattr(mod, epyk_engine.config['endpoints']['blueprints'][endpoint]['name']))

def __init_test():
  mod = importlib.import_module('epyk_basic_endpoints')
  app.register_blueprint(getattr(mod, epyk_engine.config['endpoints']['blueprints']['epyk_basic_endpoints']['name']))


if __name__ == '__main__':
  epyk_engine.init()
  __init_test()
  app.run(host=epyk_engine.config['host']['ip'], port=epyk_engine.config['host']['port'], threaded=True)