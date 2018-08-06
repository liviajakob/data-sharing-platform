"""
This script writes the configuration file config.conf
File: write_config.py

@author: livia
"""

from configobj import ConfigObj
import os, sys
config = ConfigObj()

config.filename = "config.conf"

# get absolute module directory
module_path = sys.modules[__name__].__file__
dir_path = os.path.dirname(module_path)





#
config['db'] = {}
config['db']['name'] = 'metadata.db'
config['db']['type'] = 'sqlite:///'
config['db']['path'] = os.path.join(dir_path,'data', 'output')

#
config['web'] = {}
config['web']['dataset_location'] = 'http://127.0.0.1:8887'
config['web']['mapcentre'] = {'x': 30665.5, 'y': -2039176.688}
config['web']['projection'] = 'EPSG:3413' # this is the projection displayed on the client-side
config['web']['app_port'] = 5000
config['web']['api_port'] = 5002
config['web']['app_root'] = 'http://localhost'
config['web']['api_root'] = 'http://localhost'


#
config['data'] = {}
config['data']['input'] = os.path.join(dir_path,'data', 'input')
config['data']['output'] = os.path.join(dir_path,'data', 'output','datasets')
config['data']['tiles'] = 'tiles'
config['data']['projection'] = 'EPSG:3413' #this is the projection all the data is converted to for display

#
config['layers'] = {}
config['layers']['rawfilename'] = 'raw_input'
config['layers']['reprojectedfilename'] = 'reproject'
config['layers']['types'] = ['dem', 'rate', 'error', 'velocity', 'radar_backscatter']
config['layers']['scale']=[{'min': 0, 'max': 3000},{'min': -1, 'max': 1},{'min': 0, 'max': 3000}, {'min': 0, 'max': 100}, {'min': 0, 'max': 255}]
config['layers']['colours'] = [config['layers']['types'][0]+'.txt', config['layers']['types'][1]+'.txt', config['layers']['types'][2]+'.txt', config['layers']['types'][3]+'.txt', config['layers']['types'][4]+'.txt']
config['layers']['colourmethods'] = ['linear', 'centred', 'linear', 'linear', 'linear'] # method how the colours are computed
config['layers']['colpath'] = os.path.join(config['data']['input'], 'colourfiles')

# checks
assert len(config['layers']['types'])==len(config['layers']['scale'])
assert len(config['layers']['types'])==len(config['layers']['colours'])


#
config.write()