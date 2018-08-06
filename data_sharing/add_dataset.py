'''
Command line interface to add a new dataset
File: add_dataset.py

usage: add_dataset.py [-h] [-min min] [-max max] [-a layerfile layertype date]
                                [-c cite] [--version]
                                layerfile layertype date


description: register a new dataset.

positional arguments:
  layerfile                     filename of the first layer:
  layertype                     choices = {dem, rate, error, velocity} ||| type of the
                                layer
  date                          date of the first layer - format YYYY-MM-DD

optional arguments:
  -h, --help                    show this help message and exit
  -min min                      saturation minimum for colouring the raster file of
                                layer1 ||| if not provided the default for this
                                layertype is used
  -max max                      saturation maximum for colouring the raster file of
                                layer1 ||| if not provided the default for this
                                layertype is used
  -a layerfile layertype date
                                Additional Layer: [filename, filetype, date] with
                                filetype choices = ['dem', 'rate', 'error',
                                'velocity'] ||| Any number of additional layers can be
                                given as input
  -c cite                       How to cite this dataset (Description)
  --version                     Show program's version number


@author: livia
'''

import argparse
from definitions import CONFIG_PATH
from configobj import ConfigObj
from display_data.rollback import Rollback
from display_data.ingestion import Ingestion, DatasetCreator
import logging
import traceback
from datetime import datetime


def handle_input():
    '''Checks and converts sys.args
    starts the command if the input is correct
    
    '''
    layer_metavar = ('layerfile','layertype', 'date')

    #configuration file
    config = ConfigObj(CONFIG_PATH)
    types = config['layers']['types'] ## read from config file
    
    parser = argparse.ArgumentParser(description='description: register a new dataset.')
    parser.add_argument('layerfile1', action='store', metavar='layerfile',
                help='filename of the first layer:')
    parser.add_argument('layertype1', action='store', choices=types, metavar='layertype',
                help='choices = {%(choices)s} || type of the layer')
    parser.add_argument('date1', action='store', metavar='date', type=valid_date,
                help='date of the first layer - format YYYY-MM-DD') 
    parser.add_argument('-min', action='store', metavar='min', type=float,
                help='saturation minimum for colouring the raster file of layer1 || if not provided the default for this layertype is used')
    parser.add_argument('-max', action='store', metavar='max', type=float,
                help='saturation maximum for colouring the raster file of layer1 || if not provided the default for this layertype is used')
    parser.add_argument('-a', dest='additional', action='append',nargs=len(layer_metavar), metavar=layer_metavar,
                help='Additional Layer: [filename, filetype, date] with filetype choices = {} ||| Any number of additional layers can be given as input'.format(types))
    parser.add_argument('-c', dest="cite", metavar='cite', action='store', 
                help='How to cite this dataset (Description)')
    parser.add_argument('--version', action='version', version='Version 1.0, Not released yet.', help="Show version number")

    args = parser.parse_args()
    
    firstlayer = {layer_metavar[0] : args.layerfile1, layer_metavar[1] : args.layertype1, layer_metavar[2] : args.date1, 'min' : args.min, 'max' : args.max}
    kwargs={'cite': args.cite}
    
    if args.additional is None:
        args.additional = [] # no additional layers
    layerTypeConstraintMet(args.additional, types) # check if constraint met
    layers=[]
    for lyr in args.additional:
        dic = {}
        for index, item in enumerate(layer_metavar):
            dic[item] = lyr[index]
        layers.append(dic)
        
    layers.insert(0,firstlayer)
    kwargs['layers'] = layers
    add_dataset(**kwargs)



def add_dataset(**kwargs):
    ''' Processes and adds a new dataset to the database and file system
    
    Input Parameters:
        kwargs - a keyword dictionary containing information to add the new dataset
        
    '''
    logging.basicConfig(level=logging.INFO) 
    logger = logging.getLogger(__name__)
    rollback = Rollback()

    try:
        ing = Ingestion(rollback, logger)
        creator = DatasetCreator(**kwargs)
        ing.create(creator)
        logger.info('Dataset successfully added!')
    except Exception as e:
        logger.info('Error encountered, rolling back...')
        rollback.rollback()
        if hasattr(e, 'message'):
            logger.error(e.message)
        else:
            logger.error(traceback.format_exc()) 
        logger.info('See the log file add_dataset.log for more information about the error')
    



def layerTypeConstraintMet(inp, types):
    '''Checks if layer type constraint is met
        
    Raises: 
        ArgumentTypeError if layertype constraint is not is not met
        
    '''
    for i in inp:
        if i[1] not in types:
            msg = "Not a valid layertype: '{0}'.".format(i[1])
            raise argparse.ArgumentTypeError(msg)
        i[2] = valid_date(i[2])



def valid_date(s):
    '''Checks if date is valid
    
    Raises: 
        ArgumentTypeError if date is not valid
    
    '''
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)



if __name__ == '__main__':
    handle_input()


