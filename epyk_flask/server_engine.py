import yaml, hashlib, sys, os, importlib



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

def hash_content(file_path):
  with open(file_path, 'rb') as f:
    f_hash = hashlib.blake2b()
    while True:
      data = f.read(8192)
      if not data:
        break

      f_hash.update(data)
  return f_hash.hexdigest()

class Engine(object):

  __instance = None
  config = None

  def __new__(cls, config_path=None):
    if cls.__instance is None:
      cls.__instance = super(Engine, cls).__new__(cls)
    return cls.__instance

  def __init__(self, config_path=None):
    if self.config is None:
      if config_path is None:
        with open('config.yaml', 'r') as f:
          self.config = yaml.load(f, Loader=yaml.FullLoader)
      else:
        with open(config_path, 'r') as f:
          self.config = yaml.load(f, Loader=yaml.FullLoader)


  def find_script(self, folder_name, script_name):
    file_path = os.path.join(self.config['default_repo']['path'], folder_name, script_name)
    if os.path.exists(file_path):
      return file_path

    else:
      for repo, repo_attr in self.config['repos'].items():
        file_path = os.path.join(repo_attr['path'], folder_name, script_name)
        if os.path.exists(file_path):
          return file_path

    return None

  def run_script(self, folder_name, script_name):
    """
    """
    if not script_name.endswith('.py'):
      full_name = '%s.py' % script_name
    else:
      full_name = script_name
      script_name = script_name.replace('.py', '')

    file_path = self.find_script(folder_name, full_name)
    if file_path:
      script_hash = hash_content(file_path)
      output_name = '%s_%s_%s' % (folder_name, script_name, script_hash)
      output_path = os.path.join(self.config['html_output'], 'html', '%s.html' % output_name)
      if os.path.exists(output_path):
        return output_path
    else:
      raise MissingScriptException('Script is missing from the repository configured %s/%s' % (folder_name, script_name))

    mod = importlib.import_module('%s.%s' % (folder_name, script_name))
    rptObj = getattr(mod, 'REPORT_OBJECT', False)
    if not rptObj:
      raise MissingRptObjException('Your report: %s is missing the REPORT_OBJECT attribute which should be an Report Object from Epyk-UI' % mod.__name__)

    if hasattr(mod, 'FAVICON'):
      rptObj.logo = mod.FAVICON
    if getattr(mod, 'CONTROLLED_ACCESS', False):
      controlLevel = getattr(mod, 'CONTROLLED_LEVEL', 'ENV').upper()

    rptObj.outs.html_file(path=self.config['html_output'], name=output_name)
    return os.path.join(self.config['html_output'], 'html', output_name)