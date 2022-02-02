import glob
import shutil
from .log import *

def get_certain_format_files_from_path(path = './', format='csv'):
  result = glob.glob('{}*.{}'.format(path, format))
  return result


def move_file(file_name, directory):
  shutil.move(file_name, directory)

# def getLogger():
#   return logger





