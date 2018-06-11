"""This script writes a configuration file"""

from configobj import ConfigObj
import os
config = ConfigObj()


config.filename = "config.conf"
#
config['keyword1'] = 'value1'
config['keyword2'] = 'value2'
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
#
section2 = {
    'keyword5': 'value5',
    'keyword6': 'value6',
    'sub-section': {
        'keyword7': 'value7'
        }
}

# @TODO query layer types from database
config['layers'] = {}
config['layers']['rawfilename'] = 'raw_input'
config['layers']['types'] = ['dem', 'rate', 'error']
config['layers']['exponent'] = [1, 5, 3]
config['layers']['scale']=[{'min': 0, 'max': 4000},{'min': -2, 'max': 2},{'min': 0, 'max': 3000}]

config['layers']['colours'] = [config['layers']['types'][0]+'.txt', config['layers']['types'][1]+'.txt', config['layers']['types'][2]+'.txt']
config['layers']['colpath'] = os.path.join(config['data']['input'], 'colourfiles')

#
config.write()