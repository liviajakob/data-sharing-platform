'''
Created on 10 May 2018

@author: livia
'''
import sys
import argparse
from definitions import CONFIG_PATH
from configobj import ConfigObj
from display_data.rollback import Rollback
from display_data.database import DatabaseIngestion
import logging


def handle_input():
    '''Checks and converts sys.args and starts the command if the input is right'''

    config = ConfigObj(CONFIG_PATH)
    types = config['layers']['types'] ## read from config file
    
    parser = argparse.ArgumentParser(description='Register a new dataset.')
    parser.add_argument('layerfile1', action='store', nargs=1,
                help='filename of the layer:')
    parser.add_argument('layertype1', action='store', nargs=1, choices=types, metavar='layertype',
                help='choices = {%(choices)s} ||| type of the layer')
    parser.add_argument('-a', dest='additional', action='append',nargs=2, metavar=('layername','layertype'), 
                help='Additional Layer: [filename, filetype] with filetype choices = {} ||| Any number of additional can be given as input'.format(types))
    parser.add_argument('-c', dest="cite", action='store', 
                help='How to cite this dataset (Description)')
    parser.add_argument('--version', action='version', version='Version 1.0, Not released yet.', help="Show program's version number")

    args = parser.parse_args()
    
    if args.additional is None:
        layers=[[args.layerfile1[0], args.layertype1[0]]]
        print('dta', layers)
        add_dataset(layers=layers, cite=args.cite)
        
    elif typeConstraintMet(args.additional, types):
        layers = args.additional
        layers.insert(0,[args.layerfile1[0], args.layertype1[0]])
        
        print('dta', layers)
        add_dataset(layers=layers, cite=args.cite)
        
    else:
        print("layertypes must have one of the following values: {} ".format(types))


def add_dataset(layers, cite):
    '''
    Input Params:
        layer: [[file1, type1],[file2, type2],[file3, type3]]
    
    '''
    logging.basicConfig(level=logging.INFO) #NOTSET gives all the levels, e.g. INFO only .info
    logger = logging.getLogger(__name__)
    rollback = Rollback(logger)

    
    try:
        ing = DatabaseIngestion(rollback, logger)
        ing.addDataset(layers, cite)
        logger.info('Success!!!')
    except:
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



