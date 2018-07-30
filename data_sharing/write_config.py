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
config['data'] = {}
config['data']['input'] = os.path.join(dir_path,'data', 'input')
config['data']['output'] = os.path.join(dir_path,'data', 'output','datasets')
config['data']['tiles'] = 'tiles'
config['data']['projection'] = 'EPSG:3413' #this is the projection all the data is converted to for display

#
config['layers'] = {}
config['layers']['rawfilename'] = 'raw_input'
config['layers']['reprojectedfilename'] = 'reproject'
config['layers']['types'] = ['dem', 'rate', 'error', 'velocity']
config['layers']['scale']=[{'min': 0, 'max': 3000},{'min': -1, 'max': 1},{'min': 0, 'max': 3000}, {'min': 0, 'max': 100}]
config['layers']['colours'] = [config['layers']['types'][0]+'.txt', config['layers']['types'][1]+'.txt', config['layers']['types'][2]+'.txt', config['layers']['types'][3]+'.txt']
config['layers']['colourmethods'] = ['linear', 'centred', 'linear', 'linear'] # method how the colours are computed
config['layers']['colpath'] = os.path.join(config['data']['input'], 'colourfiles')

# checks
assert len(config['layers']['types'])==len(config['layers']['scale'])
assert len(config['layers']['types'])==len(config['layers']['colours'])


#
config.write()