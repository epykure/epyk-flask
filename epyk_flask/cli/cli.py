"""
"""
import sys
import argparse
import pkg_resources
import shutil
import os
import importlib
from epyk_flask.cli import project_structure
from epyk_flask import server_engine



#TODO imlement install cli function to install new endpoints add ons


def main():
  """"""
  parser_map = {'new':           (create_new_parser,         '''Create new server structure'''),
                'env':           (create_env_parser,         '''Create new environemnt'''),
                'run':           (create_run_parser,         '''Deploy latest changes'''),
                'reset':         (create_reset_parser,       '''Resets parts of the environment'''),
                'clear':         (create_clear_parser,       '''Clear whole project'''),
                'version':       (create_version_parser,     '''Informs on current package version''')
                }
  arg_parser = argparse.ArgumentParser(prog='epyk-flask')
  subparser = arg_parser.add_subparsers(title='Commands', dest='command')
  subparser.required = True
  for func, parser_init in parser_map.items():
    new_parser = subparser.add_parser(func, help=parser_init[1])
    parser_init[0](new_parser)
  args = arg_parser.parse_args(sys.argv[1:])
  return args.func(args)


def create_new_parser(subparser):
  """"""
  subparser.set_defaults(func=new)
  subparser.add_argument('-p', '--path', required=True, help='''The path where the new environment will be created: -p /foo/bar''')
  subparser.add_argument('-n', '--name', default='epyk-flask', help='''The name of the new project: -n MyEnv''')
  subparser.add_argument('--from', help='''Path or URL of the epyk-flask server to be copied from: --from /foo/bar/server1 or --from http://repo/env1/server1''')

def create_env_parser(subparser):
  """"""
  subparser.set_defaults(func=env)
  subparser.add_argument('-p', '--path', required=True, help='''The path where the new environment will be created: -p /foo/bar''')
  subparser.add_argument('-n', '--name', default='NewEnv', help='''The name of the new environment: -n MyEnv''')

def create_run_parser(subparser):
  """"""
  subparser.set_defaults(func=run)
  subparser.add_argument('-p', '--path', required=True, help='''The path where the epyk-flask you want to run is: -p /foo/bar/myServer''')
  subparser.add_argument('-c', '--config_path', help='''The path where config is located, the default will point to the config folder inside your project: -c /foo/bar/config.yaml''')
  subparser.add_argument('-x', '--exclude', nargs='+', help='''Specify blueprints you want to exclude from the app: -x epyk_basic_endpoints, other_endpoints''')

def create_reset_parser(subparser):
  """"""
  subparser.set_defaults(func=reset)
  subparser.add_argument('-p', '--path', required=True, help='''Path for the project project''')
  subparser.add_argument('-n', '--name', default='epyk-flask', help='''The name of the new environment: -n MyEnv''')
  subparser.add_argument('-o', '--only', nargs='+', default=['all'], help='''Specified what you want to reset (templates, config, by default it will do both)''')

def create_clear_parser(subparser):
  """"""
  subparser.set_defaults(func=clear)
  subparser.add_argument('-p', '--path', required=True, help='''Clears whole project''')

def create_version_parser(subparser):
  """"""
  subparser.set_defaults(func=version)

def parse_struct(env_path, struct, struct_type):
  """"""
  for sub_struct in struct:
    if type(sub_struct) == dict:
      for sub_folder, struct in sub_struct.items():
        new_env_path = os.path.join(env_path, sub_folder)
        os.makedirs(new_env_path)
        parse_struct(new_env_path, struct, struct_type)
    else:
      if sub_struct == '__init__.py' or sub_struct not in os.listdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'export', struct_type)):
        open(os.path.join(env_path, sub_struct), 'w').close()
      else:
        shutil.copy(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'export', struct_type, sub_struct), env_path)

def new(args):
  """
  Creates a new epyk-flask folder structure on disk
  """
  env_path = os.path.join(args.path, args.name)
  if os.path.exists(env_path):
    raise argparse.ArgumentTypeError('An environment with this name already exists at this location: {}'.format(env_path))

  os.makedirs(env_path)
  open(os.path.join(env_path, '__init__.py'), 'w').close()
  for folder, struct in project_structure.folder_struct.items():
    new_env_path = os.path.join(env_path, folder)
    os.makedirs(new_env_path)
    parse_struct(new_env_path, struct, 'server')
  print('Environment Created!')

def env(args):
  """

  """
  pass

def run(args):
  """

  """
  sys.path.append(args.path)
  if args.config_path:
    config_path = args.config_path if args.c.endswith('.yaml') else '%s.config.yaml' % args.config_path
  else:
    config_path = os.path.join(args.path, 'config', 'config.yaml')
  engine = server_engine.Engine(config_path)
  if engine.config['app'].get('path'):
    sys.path.append(engine.config['app'].get('path'))
  mod = importlib.import_module(engine.config['app']['name'])
  mod.init_app(engine)
  mod.app.run(host=engine.config['host']['ip'], port=engine.config['host']['port'], threaded=True)

def reset(args):
  if 'all' in args.only:
    clear(args)
    new(args)
  #TODO Implement specific logic to reset parts of a project

def clear(args):
  shutil.rmtree(args.path)
  print('Environment Cleared!')

def version(args):
  """
  Returns the package version for Epyk
  """
  print('Epyk-Flask Version: %s' % pkg_resources.get_distribution('epyk-flask').version)

if __name__ == '__main__':
  main()
