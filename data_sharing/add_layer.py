'''
Created on 10 May 2018

@author: livia
'''
import sys
import argparse
from definitions import CONFIG_PATH
from configobj import ConfigObj
from display_data.rollback import Rollback
from display_data.ingestion import Ingestion, RasterLayerCreator
import logging
import os
import traceback


def handle_input():
    '''Checks and converts sys.args and starts the command if the input is right'''

    config = ConfigObj(CONFIG_PATH)
    types = config['layers']['types'] ## read from config file
    
    parser = argparse.ArgumentParser(description='Register a new layer.')
    parser.add_argument('dataset_id', action='store', type=int,
                help='ID of the dataset:')
    parser.add_argument('layerfile', action='store',
                help='filename of the layer:')
    parser.add_argument('layertype', action='store', choices=types, metavar='layertype',
                help='choices = {%(choices)s} ||| type of the layer')
    parser.add_argument('--version', action='version', version='Version 1.0, Not released yet.', help="Show program's version number")

    args = parser.parse_args()
    print('ARGS',vars(args))
    #print(args.layertype)
    add_layer(**vars(args))
        
        

def add_layer(**kwargs):
    '''
    
    '''
    logging.basicConfig(level=logging.NOTSET) #NOTSET gives all the levels, e.g. INFO only .info
    logger = logging.getLogger(__name__)
    rollback = Rollback(logger)

    
    try:
        ing = Ingestion(rollback, logger)
        creator = RasterLayerCreator(**kwargs)
        ing.create(creator)
        #ing.addLayerToDataset(filename=layerfile, ltype=layertype, dataset_id=dataset_id)
        logger.info('Success!')
    except Exception as e:
        if hasattr(e, 'message'):
            logger.error(e.message)
        else:
            logger.error(traceback.format_exc()) 
        logger.info('Rolling back...')
        rollback.rollback()
        

    
    



def typeConstraintMet(inp, types):
    '''Checks if type constraint is met
    
    Returns:
        True if it is met, False else
    '''
    for i in inp:
        if i[1] not in types:
            return False
    return True


if __name__ == '__main__':
    handle_input()

