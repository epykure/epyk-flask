from flask import Flask, Blueprint
import importlib
from epyk_flask import epyk_engine
app = Flask(__name__)



def init_flask_app(engine, excl_endpoints=None):
  for endpoint in engine.config['endpoints']['blueprints']:
    if excl_endpoints and endpoint in excl_endpoints:
      continue

    mod = importlib.import_module(endpoint)
    app.register_blueprint(getattr(mod, engine.config['endpoints']['blueprints'][endpoint]['name']))

def __init_test(engine):
  mod = importlib.import_module('epyk_basic_endpoints')
  app.register_blueprint(getattr(mod, engine.config['endpoints']['blueprints']['basic_endpoints']['name']))


if __name__ == '__main__':
  engine = epyk_engine.Engine()
  __init_test(engine)
  app.run(host=engine.config['host']['ip'], port=engine.config['host']['port'], threaded=True)