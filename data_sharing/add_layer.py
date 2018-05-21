'''
Created on 10 May 2018

@author: livia
'''
import sys
import argparse
from definitions import CONFIG_PATH
from configobj import ConfigObj
from display_data.rollback import Rollback
from display_data.ingestion import DatabaseIngestion
import logging
import os
import traceback


def handle_input():
    '''Checks and converts sys.args and starts the command if the input is right'''

    config = ConfigObj(CONFIG_PATH)
    types = config['layers']['types'] ## read from config file
    
    parser = argparse.ArgumentParser(description='Register a new layer.')
    parser.add_argument('dataset_id', action='store', nargs=1, type=int,
                help='ID of the dataset:')
    parser.add_argument('layerfile', action='store', nargs=1,
                help='filename of the layer:')
    parser.add_argument('layertype', action='store', nargs=1, choices=types, metavar='layertype',
                help='choices = {%(choices)s} ||| type of the layer')
    parser.add_argument('--version', action='version', version='Version 1.0, Not released yet.', help="Show program's version number")

    args = parser.parse_args()
    add_layer(layerfile=args.layerfile[0], layertype=args.layertype[0], dataset_id = args.dataset_id[0])
        
        

def add_layer(layerfile, layertype, dataset_id):
    '''
    
    '''
    logging.basicConfig(level=logging.NOTSET) #NOTSET gives all the levels, e.g. INFO only .info
    logger = logging.getLogger(__name__)
    rollback = Rollback(logger)

    
    try:
        ing = DatabaseIngestion(rollback, logger)
        ing.addLayerToDataset(filename=layerfile, ltype=layertype, dataset_id=dataset_id)
        print('hi')
        logger.info('Success!!!')
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
            print(e)
        else:
            print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())
        logger.info('Rolling back...')
        rollback.rollback()
        logger.info('Rolled back!!')

    
    



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

