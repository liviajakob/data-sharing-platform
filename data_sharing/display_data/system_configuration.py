'''
Created on 14 May 2018

@author: livia
'''
import logging, os, ast
from definitions import CONFIG_PATH
from configobj import ConfigObj
import shutil
    

class ConfigSystem():
    '''A class that manages the file system'''
    
    def __init__(self, logger=None, dataset_id=None):
        if logger is None:
            logging.basicConfig(level=logging.INFO) #NOTSET gives all the levels, e.g. INFO only .info
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger
        self.config = ConfigObj(CONFIG_PATH)
        self.dataset_id=dataset_id
    
    def getDataInputPath(self):
        return self.config['data']['input']
    
    
    def dbPath(self):
        settings = self.config['db']
        return os.path.join(settings['path'],settings['name'])

    def dbEngine(self):
        return self.config['db']['type']
    
    def getColourFile(self, layertype):
        '''Returns name and path to the colourfile for a given layer'''
        assert layertype in self.config['layers']['types']
        i = self.config['layers']['types'].index(layertype)
        filename = self.config['layers']['colours'][i]
        return os.path.join(self.config['layers']['colpath'], filename)
    
    def getLayerScale(self, layertype):
        '''Returns name and path to the colourfile for a given layer'''
        assert layertype in self.config['layers']['types']
        i = self.config['layers']['types'].index(layertype)
        scale = self.config['layers']['scale'][i]
        # convert to dict
        return ast.literal_eval(scale)
    
    
      
    def getExponent(self, layertype):
        assert layertype in self.config['layers']['types']
        i = self.config['layers']['types'].index(layertype)
        return float(self.config['layers']['exponent'][i])
        
    def newDatasetFolder(self, d_id=None):
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        path = self.config['data']['output']
        folder = os.path.join(path, str(d_id))
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            self.logger.info('Path already exists')
            
    def newLayerFolder(self, ltype, d_id=None):
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        folder = os.path.join(self.getDatasetFolder(d_id), ltype)
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            self.logger.info('Path already exists')
            
            
            
    def removeLayerFolder(self, ltype, d_id=None):
        '''Removes the layer directory'''
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        folder = os.path.join(self.getDatasetFolder(d_id), ltype)
        if os.path.exists(folder):
            shutil.rmtree(folder)
            self.logger.info("folder '{}' removed.".format(folder))
        else:
            self.logger.error("folder '{}' doesn't exist.".format(folder))  
        
        
        
    def removeDatasetFolder(self, d_id=None):
        '''Removes the dataset directory'''
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        path = self.config['data']['output']
        folder = os.path.join(path, str(d_id))
        if os.path.exists(folder):
            shutil.rmtree(folder)
        else:
            self.logger.info("folder '{}' doesn't exist.".format(folder))
    
    def getDatasetFolder(self, d_id=None):
        '''Returns the path to a dataset folder'''
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        path = self.config['data']['output']
        folder = os.path.join(path, str(d_id))
        assert os.path.exists(folder)
        return folder
 
    def getLayerFolder(self, ltype, d_id=None):
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        folder = os.path.join(self.getDatasetFolder(d_id), ltype)
        assert os.path.exists(folder)
        return folder
    
    def getTilesFolder(self, ltype, d_id=None):
        folder = os.path.join(self.getLayerFolder(ltype=ltype, d_id=d_id), self.config['data']['tiles'])
        return folder
    