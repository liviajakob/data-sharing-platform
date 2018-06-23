'''
Created on 10 May 2018

@author: livia
'''
import sys
import argparse
from definitions import CONFIG_PATH
from configobj import ConfigObj
from display_data.rollback import Rollback
from display_data.ingestion import Ingestion, DatasetCreator
import logging
import os, traceback


def handle_input():
    '''Checks and converts sys.args and starts the command if the input is right'''

    layer_metavar = ('layerfile','layertype')


    config = ConfigObj(CONFIG_PATH)
    types = config['layers']['types'] ## read from config file
    
    parser = argparse.ArgumentParser(description='Register a new dataset.')
    parser.add_argument('layerfile1', action='store',
                help='filename of the layer:')
    parser.add_argument('layertype1', action='store', choices=types, metavar='layertype',
                help='choices = {%(choices)s} ||| type of the layer')
    parser.add_argument('-a', dest='additional', action='append',nargs=len(layer_metavar), metavar=layer_metavar, 
                help='Additional Layer: [filename, filetype] with filetype choices = {} ||| Any number of additional can be given as input'.format(types))
    parser.add_argument('-c', dest="cite", action='store', 
                help='How to cite this dataset (Description)')
    parser.add_argument('--version', action='version', version='Version 1.0, Not released yet.', help="Show program's version number")

    args = parser.parse_args()
    
    print(vars(args))
    
    sys.exit(0)
    
    firstlayer = {layer_metavar[0] : args.layerfile1, layer_metavar[1] : args.layertype1}
    kwargs={'cite': args.cite}
    
    if args.additional is None:
        layers=[firstlayer]
        print('dta', layers)
        kwargs['layers'] = [firstlayer]
        add_dataset(**kwargs)
    elif typeConstraintMet(args.additional, types):
        
        layers=[]
        for lyr in args.additional:
            dic = {}
            for index, item in enumerate(layer_metavar):
                dic[item] = lyr[index]
            layers.append(dic)
            
        layers.insert(0,firstlayer)
        kwargs['layers'] = layers
        add_dataset(**kwargs)
        
    else:
        print("layertypes must have one of the following values: {} ".format(types))


def add_dataset(**kwargs):
    '''
    Input Params:
        layer: [[file1, type1],[file2, type2],[file3, type3]]
    
    '''
    logging.basicConfig(level=logging.NOTSET) #NOTSET gives all the levels, e.g. INFO only .info
    logger = logging.getLogger(__name__)
    rollback = Rollback(logger)

    
    try:
        ing = Ingestion(rollback, logger)
        print('KWRAGS', kwargs)
        creator = DatasetCreator(**kwargs)
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



