'''
Command line interface to add a new layer to a dataset
File: add_layer.py


usage: add_layer.py [-h] [-min min] [-max max] [-u] [--version]
                    dataset_id layerfile layertype date

description: register a new layer.

positional arguments:
  dataset_id          id of the dataset:
  layerfile           filename of the layer:
  layertype           choices = {dem, rate, error, velocity} || type of the layer
  date                date of the layer - format YYYY-MM-DD

optional arguments:
  -h, --help          show this help message and exit
  -min min            saturation minimum for colouring the raster file || if not
                      provided the default for this layertype is used
  -max max            saturation maximum for colouring the raster file || if not
                      provided the default for this layertype is used
  -u                  force an update in case the layerfile already exists
  --version           show version number


@author: livia
'''
import argparse
from definitions import CONFIG_PATH
from configobj import ConfigObj
from display_data.rollback import Rollback
from display_data.ingestion import Ingestion, RasterLayerCreator
import logging
import traceback
from numpy.lib.tests.test_io import strptime



def handle_input():
    '''Checks and converts sys.args
    starts the command if the input is correct
    
    '''
    config = ConfigObj(CONFIG_PATH)
    types = config['layers']['types'] ## read from config file
    
    parser = argparse.ArgumentParser(description='description: register a new layer.')
    parser.add_argument('dataset_id', action='store', type=int,
                help='id of the dataset')
    parser.add_argument('layerfile', action='store',
                help='filename of the layer; the location of the file is configured in th config.conf file.')
    parser.add_argument('layertype', action='store', choices=types, metavar='layertype',
                help='choices = {%(choices)s} || type of the layer') 
    parser.add_argument('date', action='store', metavar='date', type=valid_date,
                help='date of the layer - format YYYY-MM-DD') 
    parser.add_argument('-min', action='store', metavar='min', type=float,
                help='saturation minimum for colouring the raster file || if not provided the default for this layertype is used')
    parser.add_argument('-max', action='store', metavar='max', type=float,
                help='saturation maximum for colouring the raster file || if not provided the default for this layertype is used')
    parser.add_argument('-u', dest='forceupdate', action='store_true', help='force an update in case the layerfile already exists')
    parser.add_argument('--version', action='version', version='Version 1.0, Not released yet.', help="show version number")

    args = parser.parse_args()

    add_layer(**vars(args))
    
    
        

def add_layer(**kwargs):
    ''' Processes and adds a new layer to an existing dataset
    
    Input Parameters:
        kwargs - a keyword dictionary containing information to add the new layer
        
    '''
    logging.basicConfig(level=logging.INFO) 
    logger = logging.getLogger(__name__)
    # add handler file
    handler = logging.FileHandler('add_dataset.log')
    handler.setLevel(logging.NOTSET)#NOTSET gives all the levels, e.g. INFO only .info
    rollback = Rollback()

    try:
        ing = Ingestion(rollback, logger)
        creator = RasterLayerCreator(**kwargs) 
        ing.create(creator) # create the layer
        logger.info('Layer successful added!')
    except Exception as e:
        logger.info('Error encountered, rolling back...')
        rollback.rollback()
        if hasattr(e, 'message'):
            logger.error(e.message)
        else:
            logger.error(traceback.format_exc()) 
        logger.info('See the log file add_layer.log for more information about the error')

        


def valid_date(s):
    '''Checks if date is valid
    
    Raises: 
        ArgumentTypeError if date is not valid
    
    '''
    try:
        return strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


if __name__ == '__main__':
    handle_input()

