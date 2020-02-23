from flask import Flask
import yaml, hashlib, sys, importlib, os

app = Flask(__name__)
config = None


class MissingEpykFlaskConfigException(Exception):
  """Exception to be raised when the configuration is missing"""
  pass

class MissingAttrConfig(Exception):
  """Exception to be raised when an attribute is missing from the configuration"""
  pass

def init(config_path):
  global config
  with open(config_path, 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

  for repo in config['repos']:
    sys.path.append(repo['path'])

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
      raise MissingAttrConfig('Missing attribute %s from configuration' % attr)

    if attr_len > 1:
      parse_config(attr[1], config[attr[0]])

def config_required(*dec_args):
  """Allows to check specific properties have been set before using a function"""
  global config
  def wrap(func):
    if config is None:
      raise MissingEpykFlaskConfigException('Configuration required for endpoint: %s. Set epyk_config from %s' % (func.__name__, __name__))

    for attr in dec_args:
      parse_config(attr, config)

    def inner(*args, **kwargs):
      return func(*args, **kwargs)

    return inner

  return wrap

def linked_script(folder_name='root', script_name='index'):
  """"""
  global config
  def wrap(func):
    script_hash = ''
    used_repo = config['main_repo']['name']
    file_path = os.path.join(config['main_repo']['path'], folder_name, script_name)
    if os.path.exists(file_path):
      script_hash = hash_content(file_path)
    else:
      for repo in config['repos']:
        file_path = os.path.join(repo['path'], folder_name, script_name)
        if os.path.exists(file_path):
          script_hash = hash_content(file_path)
          break

    output_file = os.path.join(config['html_output'], '%s_%s_%s_%s.html' % (used_repo, folder_name, script_name, script_hash))
    if os.path.exists(output_file):
      with open(output_file, 'r') as f:
        data = f.read()
      return data

    def inner(*args, **kwargs):
      return func(*args, **kwargs)

    return inner

  return wrap