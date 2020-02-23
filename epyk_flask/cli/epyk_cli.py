"""
"""
import sys
import argparse
import pkg_resources
import shutil
import os
import project_structure



def main():
  """"""
  parser_map = {'new':           (create_new_parser,         '''Create new server structure'''),
                'env':           (create_env_parser,         '''Create new environemnt'''),
                'run':           (create_run_parser,         '''Deploy latest changes'''),
                'reset':         (create_reset_parser,       '''Performs operation on local DB (Sqlite)'''),
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
  subparser.add_argument('-n', '--name', default='epyk-flask', help='''The name of the new environment: -n MyEnv''')
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

def create_reset_parser(subparser):
  """"""
  subparser.set_defaults(func=reset)
  subparser.add_argument('-o', '--only', nargs='+', default=['all'], help='''Specified what you want to reset (templates, config, by default it will do both)''')

def create_version_parser(subparser):
  """"""
  subparser.set_defaults(func=version)

def parse_struct(env_path, struct):
  """"""
  for sub_struct in struct:
    if type(sub_struct) == dict:
      for sub_folder, struct in sub_struct.items():
        new_env_path = os.path.join(env_path, sub_folder)
        os.makedirs(new_env_path)
        parse_struct(new_env_path, struct)
    else:
      if sub_struct == '__init__.py' or sub_struct not in os.listdir(os.path.abspath(os.path.dirname(__file__))):
        open(os.path.join(env_path, sub_struct), 'w').close()
      else:
        shutil.copyfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), sub_struct), env_path)

def new(args):
  """
  Creates a new epyk-flask folder structure on disk
  """
  env_path = os.path.join(args.path, args.name)
  if os.path.exists(env_path):
    raise argparse.ArgumentTypeError('An environment with this name already exists at this location: {}'.format(env_path))

  os.makedirs(env_path)
  for folder, struct in project_structure.folder_struct.items():
    new_env_path = os.path.join(env_path, folder)
    os.makedirs(new_env_path)
    parse_struct(new_env_path, struct)
  print('Environment created!')

def env(args):
  """

  """

def run(args):
  """

  """
  pass

def reset(args):
  pass

def version(args):
  """
  Returns the package version for Epyk
  """
  print('Epyk-Flask Version: %s' % pkg_resources.get_distribution('epyk-flask').version)

if __name__ == '__main__':
  main()
