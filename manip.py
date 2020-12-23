import shutil, os
from configparser import ConfigParser
file = 'config.ini'
config = ConfigParser()
config.read(file)

dst_dir = config['param']['path_backup']

image = config['param']['image']


shutil.copy(image, dst_dir)

