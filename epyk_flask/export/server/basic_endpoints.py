import os, sys, json, importlib, inspect
from epyk_flask import server_engine
from flask import send_from_directory, Blueprint, request
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

@basic.route("/data/get", methods=['POST'])
def get_data():
  """
  Description:
  ------------
  Endpoint for rpc/rest services
  """

  mandatory_fields = ['function', 'module', 'path']
  if request.data:
    data = json.loads(request.data)
  else:
    data = request.json if request.json else dict(request.form)
  for field in mandatory_fields:
    if field not in data:
      return json.dumps({'error': 'Missing one of more mandatory fields in data: %s' ', '.join(mandatory_fields)}), 400

  if data['path'] not in sys.path:
    sys.path.append(data['path'])

  mod = importlib.import_module(data['module'])
  func = getattr(mod, data['function'])
  defined_args = inspect.getfullargspec(func)[:4]
  need_args = False
  for i in range(3):
    if defined_args[i]:
      need_args = True
      break

  if need_args:
    args, varargs, varkw, defaults = defined_args
    len_defaults = len(defaults) if defaults else 0
    params = data.get('extra_params', {})
    def_args = {}
    try:
      if defaults:
        func_args = [params[arg] for arg in args[:-len_defaults]]
        for i, default in enumerate(args[-len_defaults:]):
          def_args[default] = params[default] if default in params else defaults[i]
      else:
        func_args = [params[arg] for arg in args]
    except KeyError as e:
      return json.dumps({'error': str(e)}), 400

    def_args.update(params.get(varkw, {}))
    func_args.extend(params.get(varargs, []))
    try:
      result = func(*func_args, *params.get(varargs, []), **def_args)
    except Exception as e:
      return json.dumps({'error': str(e)}), 400

  else:
    try:
      result = func()
    except Exception as e:
      return json.dumps({'error': str(e)}), 400

  if result:
    return json.dumps(result), 200

  else:
    return json.dumps({'status': 'success'}), 200
