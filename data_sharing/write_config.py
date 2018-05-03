"""This script writes a configuration file"""

from configobj import ConfigObj
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
config['data']['output'] = config['db']['path']+'/datasets'
#
section2 = {
    'keyword5': 'value5',
    'keyword6': 'value6',
    'sub-section': {
        'keyword7': 'value7'
        }
}
config['section2'] = section2
#
config['section3'] = {}
config['section3']['keyword 8'] = ['value8', 'value9', 'value10']
config['section3']['keyword 9'] = ['value11', 'value12', 'value13']
#
config.write()