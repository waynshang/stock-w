import glob
import shutil

def get_certain_format_files_from_path(path = './', format='csv'):
  result = glob.glob('{}*.{}'.format(path, format))
  return result


def move_file(file_name, directory):
  shutil.move(file_name, directory)

def get_keys(x):
  print("=====================")
  print(x)
  if type(x) == list:
    map_keys = map(lambda y: list(y.keys())[0], x)
    return list(map_keys)
  else:
    return list(x.keys())

def get_values(x):
  if type(x) == list:
    map_keys = map(lambda y: list(y.values())[0], x)
    return list(map_keys)
  else:
    return list(x.values())

def create_dict_from_variables(keys, values):
  d = {}
  for index, key in enumerate(keys):
    d[key] = values[index]
  return d


