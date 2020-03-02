from epyk_flask import server_engine
from flask import send_from_directory, Blueprint
import os
basic = Blueprint('basic', __name__)

@basic.route("/")
@basic.route("/index")
def index():
  try:
    result = server_engine.run_script('root', 'index')
    dirname = os.path.dirname(result)
    filename = os.path.basename(result)
    return send_from_directory(dirname, '%s.html' % filename)

  except:
    return 'FAIL', 500

@basic.route("/run/<folder_name>", defaults={'script_name': 'index'}, methods=['GET'])
@basic.route("/run/<folder_name>/<script_name>", methods=['GET'])
def run_report(folder_name, script_name):
  try:
    result = server_engine.run_script(folder_name, script_name)
    dirname = os.path.dirname(result)
    filename = os.path.basename(result)
    return send_from_directory(dirname, filename)

  except:
    return 'FAIL', 500

