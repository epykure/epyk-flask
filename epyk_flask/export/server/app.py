from flask import Flask
import importlib
from epyk_flask import server_engine
app = Flask(__name__)


def init_app(engine, excl_endpoints=None):
  print(engine.config)
  for endpoint, properties in engine.config['endpoints']['blueprints'].items():
    if excl_endpoints and endpoint in excl_endpoints:
      continue

    print(endpoint)
    path = '%s.%s' % (properties['path'], endpoint) if properties.get('path') else endpoint
    mod = importlib.import_module(path)
    app.register_blueprint(getattr(mod, engine.config['endpoints']['blueprints'][endpoint]['name']))

def __init_test(engine):
  mod = importlib.import_module('basic_endpoints')
  app.register_blueprint(getattr(mod, engine.config['endpoints']['blueprints']['basic_endpoints']['name']))


if __name__ == '__main__':
  engine = server_engine.Engine()
  __init_test(engine)
  app.run(host=engine.config['host']['ip'], port=engine.config['host']['port'], threaded=True)