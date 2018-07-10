"""This script writes a configuration file"""

from configobj import ConfigObj
import os, math
config = ConfigObj()


config.filename = "config.conf"
#

config['db'] = {}
config['db']['name'] = 'metadata.db'
config['db']['type'] = 'sqlite:///'
config['db']['path'] = '/Users/livia/msc_dissertation/CODE/data_sharing/data/output'
#
config['data'] = {}
config['data']['input'] = '/Users/livia/msc_dissertation/CODE/data_sharing/data/input'
config['data']['output'] = os.path.join(config['db']['path'],'datasets')
config['data']['tiles'] = 'tiles'
config['data']['projection'] = 'EPSG:3413' #this is the projection all the data is converted to for display

#

config['layers'] = {}
config['layers']['rawfilename'] = 'raw_input'
config['layers']['reprojectedfilename'] = 'reproject'
config['layers']['types'] = ['dem', 'rate', 'error', 'velocity']
config['layers']['exponent'] = [1, 0.5, 0.2, 4]
config['layers']['scale']=[{'min': 0, 'max': 3000},{'min': -1, 'max': 1},{'min': 0, 'max': 3000}, {'min': 0, 'max': 100}]

config['layers']['colours'] = [config['layers']['types'][0]+'.txt', config['layers']['types'][1]+'.txt', config['layers']['types'][2]+'.txt', config['layers']['types'][3]+'.txt']
config['layers']['colpath'] = os.path.join(config['data']['input'], 'colourfiles')



# calculate tile reference




#
config.write()