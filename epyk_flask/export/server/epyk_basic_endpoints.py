import epyk_engine
from flask import send_from_directory
import traceback
import os
app = epyk_engine.register(__name__)
flask_app = epyk_engine.engine_app.app

@epyk_engine.config_required
@app.route("/")
@app.route("/index")
def index():
  try:
    print('toto')
    result = epyk_engine.run_script('root', 'index')
    dirname = os.path.dirname(result)
    filename = os.path.basename(result)
    return send_from_directory(dirname, '%s.html' % filename)

  except:
    print(traceback.format_exc())
    return 'FAIL', 500

@epyk_engine.config_required
@app.route("/run/<folder_name>", defaults={'script_name': 'index'}, methods=['GET'])
@app.route("/run/<folder_name>/<script_name>", methods=['GET'])
def run_report(folder_name, script_name):
  try:
    result = epyk_engine.run_script(folder_name, script_name)
    dirname = os.path.dirname(result)
    filename = os.path.basename(result)
    return send_from_directory(dirname, filename)

  except:
    return 'FAIL', 500

