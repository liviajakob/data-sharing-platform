'''
Responsible for system and filestructure configuration, uses the config file
File: system_configuration.py

Contains:
    ConfigSystem       – Manages the file system and the config file

@author: livia
'''
import logging, os, ast
from definitions import CONFIG_PATH
from configobj import ConfigObj
import shutil, glob
import datetime
    

class ConfigSystem():
    '''
    A class managing:
        read configuration file parameter (config.conf)
        file system and folder pattern structure
    '''
    
    def __init__(self, logger=None, dataset_id=None):
        '''Constructor of ConfigSystem
        
        Input Parameter:
            logger – (optional) a python logging object
            dataset_id (int) – (optional) id of the configured dataset
        '''
        if logger is None:
            logging.basicConfig(level=logging.INFO) #NOTSET gives all the levels, e.g. INFO only .info
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger
        self.config = ConfigObj(CONFIG_PATH)
        self.dataset_id=dataset_id
        
        
    def setDatasetid(self, dataset_id):
        '''Sets self.datasetid
        
        Input Parameter:
            dataset_id (int) - the ID of the configured dataset
        '''
        self.dataset_id=dataset_id
    
    
    def getProjection(self):
        '''Returns the projection from the config file
        
        Returns:
            projection (String) – e.g. ESPG:3454
        '''
        return self.config['data']['projection']
    
    
    def getDataInputPath(self):
        '''Returns path of the data input from the config file
        
        Returns:
            path (String) – the path where the input data is located
        '''
        return self.config['data']['input']
    
    
    def getDataOutputPath(self):
        '''Returns path of the data output from the config file
        
        Returns:
            path (String) – the path where the output data is located
        '''
        return self.config['data']['output']
    
    
    def dbPath(self):
        '''Returns path (inc. filname) to the database from the config file
        
        Returns:
            path (String) – the path where the database is located
        '''
        settings = self.config['db']
        return os.path.join(settings['path'],settings['name'])

    def dbEngine(self):
        '''Returns the database engine type
        
        Returns:
            enginetype (String) – the database engine, e.g. 'sqlite:///'
        '''
        return self.config['db']['type']
    
    
    def getColourFileTemplate(self, layertype):
        '''Returns path with (inc. filename) to the colourfile template for a given layertype
        
        Input Parameter:
            layertype (String) – type of a layer, e.g. 'dem', options configured in config file
        
        Returns:
            path (String) – the path where the sample colourfile of a layertype is located
        '''
        assert layertype in self.config['layers']['types']
        i = self.config['layers']['types'].index(layertype)
        filename = self.config['layers']['colours'][i]
        return os.path.join(self.config['layers']['colpath'], filename)
    
    
    def getLayerScale(self, layertype):
        '''Returns saturation scale for a layertype from the config file
        
        Input Parameter:
            layertype (String) – type of a layer, e.g. 'dem', options configured in config file
        
        Returns:
            scale (dict) – the saturation scale, e.g. {'min': -2,'max': 2}
        '''
        assert layertype in self.config['layers']['types']
        i = self.config['layers']['types'].index(layertype)
        scale = self.config['layers']['scale'][i]
        # convert to dict
        return ast.literal_eval(scale)
    
    
    def getLayerRawFile(self, ltype, d_id, date, proj=False):
        '''Returns path with name of the raw file of a layer
        If proj is set to true the reprojected file path is returned
        
        Input Parameter:
            ltype (String) – type of the layer, e.g. 'dem', options configured in config file
            d_id (int) – dataset id of the layers layergroup
            date (datetime.datetime) – date of the layer
            proj – boolean (default: False), set to True the reprojected file path is returned
        
        Returns:
            filepath (String) – the path of the file
        '''
        pth = self.getLayerFolderByAttributes(ltype, date, d_id=d_id)
        # get file with any extension
        fname=''
        if proj:
            fls= glob.glob(os.path.join(pth,self.getReprojectedFilename())+".*")
        else:
            fls = glob.glob(os.path.join(pth,self.getRawInputFilename())+".*")
        for file in fls:
            fname=file
            break
        return os.path.join(pth,fname)
    
        
    def newDatasetFolder(self, d_id=None):
        '''Creates a new dataset folder

        Input Parameter:
            d_id (int) – (default: self.dataset_id) the dataset id
            
        '''
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        path = self.config['data']['output']
        folder = os.path.join(path, str(d_id))
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            self.logger.info('Path already exists')
    
            
    def newLayerFolder(self, layergroup, date):
        '''Creates a new layer folder

        Input Parameter:
            layergroup – a LayerGroup / RasterLayerGroup object
            date (datetime.datetime) – date of the layer
            
        '''
        d_id = layergroup.dataset_id
        folder = os.path.join(self.getDatasetFolder(d_id), layergroup.layertype, self.dateToString(date))
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            self.logger.info('Path already exists')
        
        
    def newLayerGroupFolder(self, layergroup):
        '''Creates a new layergroup folder

        Input Parameter:
            layergroup – a LayerGroup / RasterLayerGroup object
            
        '''
        d_id = layergroup.dataset_id
        folder = os.path.join(self.getDatasetFolder(d_id), layergroup.layertype)
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            self.logger.info('Path already exists')
             
            
    def removeFolder(self, folder):
        '''Removes a given folder from the directory

        Input Parameter:
            folder – the folder (inc. path) to be removed
            
        '''
        if os.path.exists(folder):
            shutil.rmtree(folder)
            self.logger.info("folder '{}' removed.".format(folder))
        else:
            self.logger.error("folder '{}' doesn't exist.".format(folder))  
            
        
    def removeDatasetFolder(self, d_id=None):
        '''Removes the dataset directory
        
        Input Parameter:
            d_id (int) – (default: self.dataset_id) the dataset id
        
        '''
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
        '''Returns the path to a dataset

        Input Parameter:
            d_id (int) – (default: self.dataset_id) dataset id of the layers layergroup

        Returns:
            folderpath (String) – the path of the folder
        '''
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        path = self.config['data']['output']
        folder = os.path.join(path, str(d_id))
        assert os.path.exists(folder)
        return folder
 
 
    def getLayerFolderByAttributes(self, ltype, date, d_id=None):
        '''Returns the path to a layergroup (layertype)

        Input Parameter:
            ltype (String) – type of the layer, e.g. 'dem', options configured in config file
            date (datetime.datetime) – date of the layer
            d_id (int) – (default: self.dataset_id) dataset id of the layers layergroup

        Returns:
            folderpath (String) – the path of the folder
        '''
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        if isinstance(date, datetime.date):
            date = self.dateToString(date)
        folder = os.path.join(self.getDatasetFolder(d_id), ltype, date)
        #assert os.path.exists(folder)
        return folder
    
    
    def getLayerGroupFolderByAttributes(self, ltype, d_id=None):
        '''Returns the path to a layergroup (layertype)
        
        Input Parameter:
            ltype (String) – type of the layer, e.g. 'dem', options configured in config file
            d_id (int) – (default: self.dataset_id) dataset id of the layers layergroup
        
        Returns:
            folderpath (String) – the path of the folder
        '''
        if d_id is None:
            assert self.dataset_id is not None
            d_id = self.dataset_id
        folder = os.path.join(self.getDatasetFolder(d_id), ltype)
        return folder
    
    
    def getLayerGroupFolder(self, layergroup):
        '''Returns the folderpath of a layergroup
        
        Input Parameter:
            layergroup – a LayerGroup / RasterLayerGroup object
        
        Returns:
            folderpath (String) – the path of the folder
        '''
        d_id = layergroup.dataset_id
        folder = os.path.join(self.getDatasetFolder(d_id), layergroup.layertype)
        return folder
    
    
    def getLayerFolders(self, layergroup):
        '''Returns the folderpaths of layers within a layergroup

        Input Parameter:
            layergroup – a LayerGroup / RasterLayerGroup object
        
        Returns:
            folderpaths (list) – a list of folderpaths
        '''
        wkdir = self.getLayerGroupFolder(layergroup)
        content = next(os.walk(wkdir))
        folders=[]
        for folder in content[1]:
            folders.append(os.path.join(content[0], folder))
        return folders
    
     
    def getLayerDates(self, layergroup):
        '''Returns the dates of layers within a layergroup

        Input Parameter:
            layergroup – a LayerGroup / RasterLayerGroup object
        
        Returns:
            dates (list) – a list of dates (in string format), e.g. ['2018-05-26','2018-05-27']
        '''
        wkdir = self.getLayerGroupFolder(layergroup)
        content = next(os.walk(wkdir))
        dates=[]
        for folder in content[1]:
            dates.append(folder)
        return dates
    
    
    def getTilesFolder(self, ltype, date, d_id=None):
        '''Returns the path to a tile layers folder of a layer

        Input Parameter:
            ltype (String) – type of the layer, e.g. 'dem', options configured in config file
            date (datetime.datetime) – date of the layer
            d_id (int) – (default: self.dataset_id) dataset id of the layers layergroup
        
        Returns:
            folderpath (String) – the path of the folder
        '''
        folder = os.path.join(self.getLayerFolderByAttributes(ltype=ltype, date=date, d_id=d_id), self.config['data']['tiles'])
        return folder
    
    
    def getLayerGroupsColourfile(self, layergroup):
        '''Returns the path to a colourfile of a layergroup

        Input Parameter:
            layergroup – a LayerGroup / RasterLayerGroup object
        
        Returns:
            filepath (String) – the path of the file
        '''
        path = os.path.join(self.getLayerGroupFolder(layergroup), 'colourfile.txt')
        return path
    
    
    def getRelativeTilesFolder(self, layergroup, date):
        '''Returns the relative path to a layers tiles
        The absolute root path is removed

        Input Parameter:
            layergroup – a LayerGroup / RasterLayerGroup object
            date (datetime.datetime) – date of the layer
        
        Returns:
            folderpath (String) – the path of the folder, e.g. 2/dem/2018-05-05/tiles
        '''
        abs_path = self.getTilesFolder(layergroup.layertype, date, layergroup.dataset_id)
        prefix = self.getDataOutputPath()
        rel_path = os.path.relpath(abs_path, prefix)
        return rel_path
    
    
    def getLayerTypes(self):
        '''Returns the layertypes from the config file

        Returns:
            layertypes (list) – a list of the layertypes
        '''
        return self.config['layers']['types']
    

    
    ## Helper methods
    
    def dateToString(self, date):
        '''Converts a datetime.date object to a String of the format YYYY-MM-DD
        
        Input Parameter:
            date (datetime.date) - a datetime object to be converted
            
        Returns:
            date (String) – of the format YYYY-MM-DD   
        '''
        if isinstance(date, datetime.date):
            date = str(date.strftime("%Y-%m-%d"))
        return date
    
    
    def getRawInputFilename(self):
        '''Returns filename of the raw data file from the config file
        
        Returns:
            filename (String) – the standard filename assigned to the raw data
        '''
        return self.config['layers']['rawfilename']
    
    
    def getReprojectedFilename(self):
        '''Returns filename of the reprojected data file from the config file
        
        Returns:
            filename (String) – the standard filename assigned to the reprojected data
        '''
        return self.config['layers']['reprojectedfilename']
    
    
