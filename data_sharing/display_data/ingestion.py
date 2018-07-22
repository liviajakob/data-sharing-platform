'''
Responsible for data processing and database ingestion
File: ingestion.py

Contains:
    Ingestion             – Initialises the ingestion
    Creator               – Abstract interface to ingest a dataset or layer
    DatasetCreator        – Inherits from Creator
    RasterLayerCreator    – Inherits from Creator


@author: livia
'''

import os
import shutil
from display_data.prepare_raster import RasterLayerProcessor, RasterTiler
from display_data.system_configuration import ConfigSystem
from display_data.database import Database
from display_data.compute_colours import ColourFactory
import abc
    
    
class Ingestion(object):
    '''Handles and initialises the ingestion of a dataset or a layer
    
    '''
    
    def __init__(self, rollback, logger, database=None):
        '''Constructor of the Ingestion class
        
        Input Parameters:
            rollback - a Rollback object
            logger - a python logger
            database - (optional) a Database object
        
        '''
        if database is None:
            self._db = Database(logger=logger) #use the standard settings from the config file
        else:
            self._db = database
        
        self.rollback = rollback
        self.logger=logger
    
    
    def create(self, creator):
        '''Creates and processes new data
        What the method creats depends on the type of creator given
        
        Input Paramters:
            creator - an instance of a class inheriting the Creator object
        
        '''
        self._db.scopedSession()
        self.rollback.addCommand(self._db.closeSession)
        creator.addConfiguration(database=self._db, logger=self.logger, rollback=self.rollback)
        creator.create() # create data here
        self._db.commit()
        self._db.closeSession()
        
        


class Creator(abc.ABC):
    '''Abstract interface for creators
    
    Child classes must include:
        create(self)
    '''
    
    @abc.abstractmethod
    def create(self):
        '''Abstract create method
        Should implement data processing and creation
        '''
        pass
    
    def addConfiguration(self, database, logger, rollback):
        '''Configures the creator
        
        Input Parameter:
            database – a Database object
            logger - a python logging object
            rollback - a Rollback object
        
        '''
        self._db = database
        self.rollback = rollback
        self.logger = logger




#############################################################


class DatasetCreator(Creator):
    '''Creates a new dataset with layers
    Manages database ingestion and data processing
    
    '''
    
    def __init__(self, **kwargs):
        '''Constructor of DatasetCreator
        
        Input Parameter:
            **kwargs – keyword dictionary containig ingestion information
                required keywords:
                    cite (str): information on how to cite the dataset
                    layers (list): list with layers
        '''
        self.conf = ConfigSystem()
        self.cite = kwargs['cite']
        self.layers = kwargs['layers']
        self.projection = self.conf.getProjection()
        
         
    
    def create(self):
        '''Creates a new dataset with layers
        
        '''
        dataset = self._db.newDataset(cite=self.cite, projection=self.projection, commit=False)
        self.conf.setDatasetid(dataset.id)
        self.conf.newDatasetFolder()
        self.rollback.addCommand(self.conf.removeDatasetFolder, {'d_id':dataset.id})
        self.addBoundingBox(dataset)
        self.addArea(dataset)
        
        # create layers
        for l in self.layers:
            l['dataset_id'] = dataset.id
            l['dataset'] = dataset
            creator = RasterLayerCreator(**l) # new creator for each layer
            creator.addConfiguration(self._db, self.logger, self.rollback)
            creator.create()
            

        
    def addBoundingBox(self, dataset):
        '''adds a bounding box to the dataset database entry
        
        Input Parameter:
            dataset – a Dataset object to which the bounding box is added
        
        '''
        assert len(self.layers) > 0
        # take the first layer
        file_extension = os.path.splitext(self.layers[0]['layerfile'])[1]
        srcf = os.path.join(self.conf.getDataInputPath(), self.layers[0]['layerfile'])
        rast_proc = RasterLayerProcessor(self.logger)
        
        repr_file = 'reproject.'+file_extension
        repr_filepath = os.path.join(self.conf.getDataInputPath(), repr_file)
        rast_proc.reproject(srcf, repr_filepath)

        rast_proc.readFile(repr_filepath)
        box=rast_proc.getMinBoundingBox()        
        dataset.xmin = box['xmin']
        dataset.xmax = box['xmax']
        dataset.ymin = box['ymin']
        dataset.ymax = box['ymax']
        os.remove(repr_filepath)
        self.logger.info('Added bounding box to layer')
    
    
        
    def addArea(self, dataset):
        '''adds a bounding box to the dataset database entry
        
        Input Parameter:
            dataset – a Dataset object to which the bounding box is added
        
        '''
        dataset.area=abs((dataset.xmax-dataset.xmin)*(dataset.xmax-dataset.xmin))

  
  

##############################################################  
    
class RasterLayerCreator(Creator):
    '''Prepares and creates a new raster layer
    Manages database ingestion and data processing
    
    '''
    
    def __init__(self, **kwargs):
        '''Constructor of RasterLayerCreator
        
        Input Parameter:
            **kwargs – keyword dictionary containig ingestion information
                required keywords:
                    layerfile (str): layer file name
                    layertype (str): a layertype (options specified in config.conf)
                    date (datetime): date of the layer; format YYYY-MM-DD (datetime.datetime)
                    dataset_id (int): the dataset id
                optional keywords:
                    dataset: an instance of the Dataset class representing the database entry
                    min (float/int): minimum value for saturation; default is in the config.conf file
                    max (float/int): maximum value for saturation; default is in the config.conf file
                    forceupdate (boolean): true if file update should be forced, false otherwise (default: false)
        '''

        self.layertype = kwargs['layertype']
        self.layerfile = kwargs['layerfile']
        self.dataset_id = kwargs['dataset_id']
        self.date = kwargs['date']
        
        self.dataset = None
        if 'dataset' in kwargs:
            self.dataset = kwargs['dataset']
               
        self.conf = ConfigSystem(dataset_id=self.dataset_id)
        self.layerfolder = self.conf.getLayerFolderByAttributes(self.layertype, self.date, self.dataset_id)
        self.layergroupfolder = self.conf.getLayerGroupFolderByAttributes(self.layertype, self.dataset_id)
        scale = self.conf.getScale(self.layertype)
        
        if 'min' in kwargs and kwargs['min'] is not None:
            self.min = kwargs['min']
        else:
            self.min = scale['min']           
        if 'max' in kwargs and kwargs['max'] is not None:
            self.max = kwargs['max']
        else:
            self.max = scale['max']        
        if 'forceupdate' in kwargs:
            self.forceUpdate = kwargs['forceupdate']
        else:
            self.forceUpdate = False
     
                
        
    
    def create(self):
        '''Creates and processes the raster layer
        
        '''        
        layer = self.getExistingLayerGroup() # see if database entry exist for layer group
        if layer is None:
            layer = self._db.newRasterLayerGroup(dataset_id=self.dataset_id, layerType=self.layertype, date = self.date, commit=False)
            self.conf.newLayerGroupFolder(layer)
            self.rollback.addCommand(self.conf.removeFolder, {'folder': self.layergroupfolder})
            self.conf.newLayerFolder(layer, self.date)
            self.processFile(layer)
            self.updateDatasetDates()
            
        elif not os.path.isdir(self.layerfolder):
            self.logger.info('Adding new layer.')
            self.conf.newLayerFolder(layer, self.date)
            self.rollback.addCommand(self.conf.removeFolder, {'folder': self.layerfolder})
            self.processFile(layer)
            #update the layergroup dates
            self.updateLayerGroupDates(layer)
        elif self.forceUpdate: #self.update(duplicate):
            self.logger.info('Time Layer will be updated: Update forced.')
            self.processFile(layer)
        else:
            self.logger.info('Duplicate discovered; Update is not forced.')
            msg = 'Layer with file={} , type={}, date={}, datasetid={} is not updated.'.format(self.layerfile, self.layertype, self.date, self.dataset_id)
            self.logger.info(msg)
            msg = 'Use the "-u" flag to update the layer'
            self.logger.info(msg)
        
        
        
    def processFile(self, layergroup):
        '''Processes the layergroup input file and prepares it for display
        
        Input Parameter:
            layergroup – a LayerGroup / RasterLayerGroup object
        
        Steps are:
            1. Copy original file and save in layergroup folder
            2. Reproject file to configured projection
            3. Crop nan values in raster file
            4. Dynamically compute colourfile with min and max values
            5. Colour the file
            6. Tile
        
        '''
        self.rast_proc = RasterLayerProcessor(logger=self.logger)
        file_extension = os.path.splitext(self.layerfile)[1] #extract extension
        srcf = os.path.join(self.conf.getDataInputPath(), self.layerfile)
        
        # 1. save init file in output folder
        cp = os.path.join(self.layerfolder, (self.conf.getRawInputFilename()+file_extension))
        shutil.copyfile(srcf, cp)
        
        # 2. reproject
        proj = os.path.join(self.layerfolder, (self.conf.getReprojectedFilename()+file_extension))
        self.rast_proc.reproject(inputfile=srcf, outputfile=proj)
        
        # 3. cut raster
        cut = os.path.join(self.layerfolder, ('cropped'+file_extension))
        self.rast_proc.cutRaster(inputfile=proj, outputfile=cut)
        
        # 4. compute colourfile
        col_output = self.conf.getLayerGroupsColourfile(layergroup)
        if not os.path.isfile(col_output): 
            col_inputfile = self.conf.getColourFileTemplate(self.layertype)
            col_method = self.conf.getColourMethod(self.layertype)
            # create right ColourCreator with ColourFactory
            colgen = ColourFactory().get_colourmaker(col_method, col_inputfile, col_output)
            colgen.computeColours(self.min, self.max)
                
        # 5. add colour
        col_rast = os.path.join(self.conf.getLayerFolderByAttributes(self.layertype, self.date, self.dataset_id), ('coloured'+file_extension))
        self.rast_proc.addColours(inputfile=cut, outputfile=col_rast, colourfile=col_output) # take the above computed as input
        
        # 6. tile
        tiler = RasterTiler()
        if self.dataset is None:
            self.dataset = self._db.getDatasets(filters={'id': self.dataset_id})
        zoom = tiler.calculateZoom(self.dataset.area)
        tiler.createTiles(col_rast, self.conf.getTilesFolder(self.layertype, self.date, d_id = self.dataset_id), zoom=zoom)
            
       
        
    
    def updateLayerGroupDates(self, layergroup):
        '''Updates start and end date of a layergroup within the database
        
        Input Parameter:
            layergroup – a LayerGroup/RasterLayerGroup object representing an entry within the database
        '''
        if self.date < layergroup.startdate:
            self._db.updateLayerGroupDates(layergroup, startdate=self.date, commit=False)
        elif self.date > layergroup.enddate:
            self._db.updateLayerGroupDates(layergroup, enddate=self.date, commit=False)
        self.updateDatasetDates()
    
    def updateDatasetDates(self):
        '''Updates the datasets dates (from self.dataset) within the database
        
        '''
        if self.dataset is None:
            self.dataset = self._db.getDatasets(filters={'id': self.dataset_id})
        if self.dataset.startdate is None or self.date < self.dataset.startdate:
            self._db.updateDatasetDates(self.dataset, startdate=self.date, commit=False)
        if self.dataset.enddate is None or self.date > self.dataset.enddate:
            self._db.updateDatasetDates(self.dataset, enddate=self.date, commit=False)
        
        
    def getExistingLayerGroup(self):
        '''Returns layer group if dataset with same layertype already exists
        
        Returns – LayerGroup/RasterLayerGroup object if it exists in database, None otherwise
        
        '''
        self.logger.info('Checking if layer with same layertype exists...')
        dupl = self._db.getRasterLayerGroups(filters={'dataset_id': self.dataset_id, 'layertype': self.layertype})
        if len(dupl)==0:
            return None   
        else:
            self.logger.info('Layertype already exists...')
            return dupl[0]
        
        