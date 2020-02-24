from flask import Flask, Blueprint
import yaml, hashlib, sys, os, importlib
import epyk_engine
app = Flask(__name__)



def init_flask_app(config_path):
  for endpoint in epyk_engine.config['endpoints']['blueprints']:
    mod = importlib.import_module(endpoint)
    app.register_blueprint(getattr(mod, epyk_engine.config['endpoints']['blueprints'][endpoint]['attr_name']))

def __init_test():
  mod = importlib.import_module('epyk_basic_endpoints')
  app.register_blueprint(getattr(mod, epyk_engine.config['endpoints']['blueprints']['epyk_basic_endpoints']['attr_name']))

def init_bp(name):
  print('toto')
  bp_config = epyk_engine.config['endpoints']['blueprints'][name]
  basic_blueprint = Blueprint(bp_config['name'], bp_config['import_name'], **{k: v for k, v in bp_config.items() if k not in ['name', 'import_name', 'attr_name']})
  return basic_blueprint

def engine_register(*args):
  return init_bp(args[0])


if __name__ == '__main__':
  epyk_engine.init()
  __init_test()
  app.run(host=epyk_engine.config['host']['ip'], port=epyk_engine.config['host']['port'], threaded=True)