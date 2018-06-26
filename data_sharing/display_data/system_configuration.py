'''
Created on 14 May 2018

@author: livia
'''
import logging, os, ast
from definitions import CONFIG_PATH
from configobj import ConfigObj
import shutil, glob
    

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
        
        
    def setDatasetid(self, dataset_id):
        '''Sets self.datasetid'''
        self.dataset_id=dataset_id
    
    
    def getProjection(self):
        return self.config['data']['projection']
    
    def getDataInputPath(self):
        return self.config['data']['input']
    
    def getDataOutputPath(self):
        return self.config['data']['output']
    
    
    def dbPath(self):
        settings = self.config['db']
        return os.path.join(settings['path'],settings['name'])

    def dbEngine(self):
        return self.config['db']['type']
    
    def getSampleColourFile(self, layertype):
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
    
    def getRawInputFilename(self):
        return self.config['layers']['rawfilename']
    
    def getReprojectedFilename(self):
        return self.config['layers']['reprojectedfilename']
    
    def getLayerTimeRawFile(self, ltype, d_id, date, proj=False):
        pth = self.getLayerTimeFolderByAttributes(ltype, date, d_id=d_id)
        # get file with any extension
        fname=''
        #print(self.getRawInputFilename()+".*")
        if proj:
            fls= glob.glob(os.path.join(pth,self.getReprojectedFilename())+".*")
        else:
            fls = glob.glob(os.path.join(pth,self.getRawInputFilename())+".*")
        for file in fls:
            fname=file
            break
        return os.path.join(pth,fname)
    
        
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
            
    def newLayerTimeFolder(self, layer, date):
        d_id = layer.dataset_id
        folder = os.path.join(self.getDatasetFolder(d_id), layer.layertype, self.dateToString(date))
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            self.logger.info('Path already exists')
        print('FOLDER', folder)
        
        
    def newLayerFolder(self, layer):
        print('LAYR', layer)
        d_id = layer.dataset_id
        folder = os.path.join(self.getDatasetFolder(d_id), layer.layertype)
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            self.logger.info('Path already exists')
        
        print('FOLDER', folder)
            
            
            
    def removeFolder(self, folder):
        '''Removes the layer directory'''
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
 
    def getLayerTimeFolderByAttributes(self, ltype, date, d_id=None):
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        date = self.dateToString(date)
        folder = os.path.join(self.getDatasetFolder(d_id), ltype, date)
        #assert os.path.exists(folder)
        return folder
    
    def getLayerFolderByAttributes(self, ltype, d_id=None):
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        folder = os.path.join(self.getDatasetFolder(d_id), ltype)
        #assert os.path.exists(folder)
        return folder
    
    
    def getLayerTimeFolder(self, layer):
        d_id = layer.dataset_id
        date = self.dateToString(layer.enddate)
        folder = os.path.join(self.getDatasetFolder(d_id), layer.layertype, date)
        #assert os.path.exists(folder)
        return folder
    
    def getLayerFolder(self, layer):
        d_id = layer.dataset_id
        folder = os.path.join(self.getDatasetFolder(d_id), layer.layertype)
        #assert os.path.exists(folder)
        return folder
    
    
    
    
    # TODO: ensure this works
    def getTimeseriesFolders(self, layer):
        #paths = []
        wkdir = self.getLayerFolder(layer)
        content = next(os.walk(wkdir))
        folders=[]
        for folder in content[1]:
            folders.append(os.path.join(content[0], folder))
        return folders
    
    
    def getTilesFolder(self, ltype, date, d_id=None):
        folder = os.path.join(self.getLayerTimeFolderByAttributes(ltype=ltype, date=date, d_id=d_id), self.config['data']['tiles'])
        return folder
    
    def getLayersColourfile(self, layer):
        '''Returns a relative path'''
        path = os.path.join(self.getLayerFolder(layer), 'colourfile.txt')
        return path
    
    def getRelativeTilesFolder(self, layer):
        abs_path = self.getTilesFolder(layer.layertype, layer.enddate, layer.dataset_id)
        prefix = self.getDataOutputPath()
        rel_path = os.path.relpath(abs_path, prefix)
        return rel_path
    
    
    def getLayerTypes(self):
        return self.config['layers']['types']
    
    
    def dateToString(self, date):
        print('DATE+', date, type(date))
        
        
        print('DATE: ', str(date.strftime("%Y-%m-%d")))
        return str(date.strftime("%Y-%m-%d"))
