import yaml, hashlib, sys, os, importlib
config = None
engine_app = None

class MissingEpykFlaskConfigException(Exception):
  """Exception to be raised when the configuration is missing"""
  pass


class MissingAttrConfigException(Exception):
  """Exception to be raised when an attribute is missing from the configuration"""
  pass


class MissingRptObjException(Exception):
  """Exception to be raised when the REPORT_OBJECT attribute is missing from a script to be run"""
  pass


class MissingScriptException(Exception):
  """Exception when a script specified couldn't be found in any repository"""
  pass


def init(config_path=None):
  global config
  global engine_app
  if config_path is None:
    with open('config.yaml', 'r') as f:
      config = yaml.load(f, Loader=yaml.FullLoader)
  else:
    with open(config_path, 'r') as f:
      config = yaml.load(f, Loader=yaml.FullLoader)

  engine_app = importlib.import_module(config['server_interface'])
  for repo, repo_attr in config['repos'].items():
    sys.path.append(repo_attr['path'])
  for path in config['endpoints']['path']:
    sys.path.append(path)

def hash_content(file_path):
  with open(file_path, 'rb') as f:
    f_hash = hashlib.blake2b()
    while True:
      data = f.read(8192)
      if not data:
        break

      f_hash.update(data)
  return f_hash.hexdigest()

def parse_config(attr, config):
  """"""
  attr_len = len(attr)
  if attr_len != 0:
    if attr[0] not in config:
      raise MissingAttrConfigException('Missing attribute %s from configuration' % attr)

    if attr_len > 1:
      parse_config(attr[1], config[attr[0]])


def config_required(*dec_args):
  """Allows to check specific properties have been set before using a function"""
  def wrap(func):
    if config is None:
      raise MissingEpykFlaskConfigException('Configuration required for endpoint: %s. Set epyk_config from %s' % (func.__name__, __name__))

    for attr in dec_args:
      parse_config(attr, config)

    def inner(*args, **kwargs):
      return func(*args, **kwargs)

    return inner

  return wrap

def find_script(folder_name, script_name):
  file_path = os.path.join(config['default_repo']['path'], folder_name, script_name)
  if os.path.exists(file_path):
    return file_path

  else:
    for repo, repo_attr in config['repos'].items():
      file_path = os.path.join(repo_attr['path'], folder_name, script_name)
      if os.path.exists(file_path):
        return file_path

  return None


def run_script(folder_name, script_name):
  """
  """
  print('tutu')
  if not script_name.endswith('.py'):
    full_name = '%s.py' % script_name
  else:
    full_name = script_name
    script_name = script_name.replace('.py', '')

  file_path = find_script(folder_name, full_name)
  print(file_path)
  if file_path:
    script_hash = hash_content(file_path)
    output_name = '%s_%s_%s' % (folder_name, script_name, script_hash)
    output_path = os.path.join(config['html_output'], 'html', '%s.html' % output_name)
    print(output_path)
    if os.path.exists(output_path):
      print('tata')
      return output_path
  else:
    raise MissingScriptException('Script is missing from the repository configured %s/%s' % (folder_name, script_name))

  mod = importlib.import_module('%s.%s' % (folder_name, script_name))
  rptObj = getattr(mod, 'REPORT_OBJECT', False)
  if not rptObj:
    MissingRptObjException('Your report: %s is missing the REPORT_OBJECT attribute which should be an Report Object from %s' % (mod.__name__, Report.__module__))
  if hasattr(mod, 'FAVICON'):
    rptObj.logo = mod.FAVICON
  if getattr(mod, 'CONTROLLED_ACCESS', False):
    controlLevel = getattr(mod, 'CONTROLLED_LEVEL', 'ENV').upper()

  rptObj.outs.html_file(path=config['html_output'], name=output_name)
  return os.path.join(config['html_output'], 'html', output_name)


def register(*args):
  return engine_app.engine_register(*args)


