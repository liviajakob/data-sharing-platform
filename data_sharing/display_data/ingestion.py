'''

@author: livia
'''

import os, time
import shutil
from display_data.prepare_raster import RasterLayerProcessor, RasterTiler
from datetime import datetime
from display_data.system_configuration import ConfigSystem
from display_data.database import Database
from display_data.compute_colours import ColourMaker
import abc
    
    
class Ingestion(object):
    '''Handles everything to ingest an new entry'''
    
    def __init__(self, rollback, logger, database=None):
        if database is None:
            self._db = Database(logger=logger) #use the standard settings from the config file
        else:
            self._db = database
        
        self.rollback = rollback
        self.logger=logger
    
    
    def create(self, creator):
        self._db.scopedSession()
        self.rollback.addCommand(self._db.closeSession)
        creator.addConfiguration(database=self._db, logger=self.logger, rollback=self.rollback)
        creator.create()
        self._db.commit()
        self._db.closeSession()
        
        





class Creator(abc.ABC):
    
    @abc.abstractmethod
    def create(self):
        pass
    
    def addConfiguration(self, database, logger, rollback):
        self._db = database
        self.rollback = rollback
        self.logger = logger


#############################################################


class DatasetCreator(Creator):
    
    
    def __init__(self, **kwargs):
        self.conf = ConfigSystem()
        self.cite = kwargs['cite']
        self.layers = kwargs['layers']
        self.projection = self.conf.getProjection() #if want to read user input --> check for var in **kwargs
        
         
    
    def create(self):
        dataset = self._db.newDataset(cite=self.cite, projection=self.projection, commit=False)
        self.conf.setDatasetid(dataset.id)
        self.conf.newDatasetFolder()
        #self.layers[0]['date']
        self.rollback.addCommand(self.conf.removeDatasetFolder, {'d_id':dataset.id})
        
        self.addBoundingBox(dataset)
        self.addArea(dataset)
        
        # create layers
        for l in self.layers:
            l['dataset_id'] = dataset.id
            l['dataset'] = dataset
            creator = RasterLayerCreator(**l)
            creator.addConfiguration(self._db, self.logger, self.rollback)
            creator.create()
            
        

        
        
    def addBoundingBox(self, dataset):
        assert len(self.layers) > 0
        ## for now just take the first layer
        file_extension = os.path.splitext(self.layers[0]['layerfile'])[1]
        srcf = os.path.join(self.conf.getDataInputPath(), self.layers[0]['layerfile'])
        rast_proc = RasterLayerProcessor(self.logger)
        
        repr_file = 'reproject.'+file_extension
        repr_filepath = os.path.join(self.conf.getDataInputPath(), repr_file)
        rast_proc.reproject(srcf, repr_filepath)
        print('reprojected')
        rast_proc.readFile(repr_filepath)
        box=rast_proc.getMinBoundingBox()        
        dataset.xmin = box['xmin']
        dataset.xmax = box['xmax']
        dataset.ymin = box['ymin']
        dataset.ymax = box['ymax']
        os.remove(repr_filepath)
        self.logger.info('ADDED BOUNDING BOX')
        
    def addArea(self, dataset):
        dataset.area=abs((dataset.xmax-dataset.xmin)*(dataset.xmax-dataset.xmin))

  
  

##############################################################  
    
class RasterLayerCreator(Creator):
    '''Prepares and creates a Layer'''
    
    def __init__(self, **kwargs):
        
        print('KWARGS', kwargs)
        print(kwargs['dataset_id'])
        
        self.layertype = kwargs['layertype']
        self.layerfile = kwargs['layerfile']
        self.dataset_id = kwargs['dataset_id']
        self.date = kwargs['date']
        
        self.dataset = None
        if 'dataset' in kwargs:
            self.dataset = kwargs['dataset']
            
            
        self.conf = ConfigSystem(dataset_id=self.dataset_id)
        self.layertimefolder = self.conf.getLayerTimeFolderByAttributes(self.layertype, self.date, self.dataset_id)
        self.layerfolder = self.conf.getLayerFolderByAttributes(self.layertype, self.dataset_id)
        scale = self.conf.getLayerScale(self.layertype)
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
        '''Creates the raster layer'''        
        layer = self.getExistingLayer()
        if layer is None:
            layer = self._db.newRasterLayer(dataset_id=self.dataset_id, layerType=self.layertype, date = self.date, commit=False)
            self.conf.newLayerFolder(layer)
            self.rollback.addCommand(self.conf.removeFolder, {'folder': self.layerfolder})
            self.conf.newLayerTimeFolder(layer, self.date)
            self.processFile(layer)
            self.updateDatasetDates()
            
        elif not os.path.isdir(self.layertimefolder):
            self.logger.info('Adding new time layer.')
            self.conf.newLayerTimeFolder(layer, self.date)
            self.rollback.addCommand(self.conf.removeFolder, {'folder': self.layertimefolder})
            self.processFile(layer)
            #update the time series dates
            self.updateTimeSeries(layer)
        elif self.forceUpdate: #self.update(duplicate):
            self.logger.info('Time Layer will be updated: Update forced.')
            self.processFile(layer)
        else:
            self.logger.info('Duplicate discovered; Update is not forced.')
            msg = 'Layer with file={} , type={}, date={}, datasetid={} is not updated.'.format(self.layerfile, self.layertype, self.date, self.dataset_id)
            self.logger.info(msg)
            msg = 'Use the "-u" flag to update the layer'
            self.logger.info(msg)
        
        
        
    def processFile(self, layer):
        '''Processes the layer input file and prepares it for display
        
        Steps are:
            1. Copy original file and save in layer folder
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
        cp = os.path.join(self.layertimefolder, (self.conf.getRawInputFilename()+file_extension))
        shutil.copyfile(srcf, cp)
        
        # 2. reproject
        proj = os.path.join(self.layertimefolder, (self.conf.getReprojectedFilename()+file_extension))
        self.rast_proc.reproject(inputfile=srcf, outputfile=proj)
        
        # 3. cut raster
        cut = os.path.join(self.layertimefolder, ('cropped'+file_extension))
        self.rast_proc.cutRaster(inputfile=proj, outputfile=cut)
        
        # 4. compute colourfile
        colfile = self.conf.getLayersColourfile(layer)
        if not os.path.isfile(colfile): 
            col_inputfile = self.conf.getSampleColourFile(self.layertype)
            colgen = ColourMaker(col_inputfile, colfile)
            colgen.computeColours(self.min, self.max)
                
        # 5. add colour
        col_rast = os.path.join(self.conf.getLayerTimeFolderByAttributes(self.layertype, self.date, self.dataset_id), ('coloured'+file_extension))
        self.rast_proc.addColours(inputfile=cut, outputfile=col_rast, colourfile=colfile) # take the above computed as input
        
        # 6. tile
        tiler = RasterTiler()
        if self.dataset is None:
            self.dataset = self._db.getDatasets(filters={'id': self.dataset_id})
        zoom = tiler.calculateZoom(self.dataset.area)
        tiler.createTiles(col_rast, self.conf.getTilesFolder(self.layertype, self.date, d_id = self.dataset_id), zoom=zoom)
            
        print('FILE: ', self.layerfile, ' TYPE: ', self.layertype, ' DATASETID', self.dataset_id)
       
        
    
    def updateTimeSeries(self, layer):
        '''Updates start and end date of a layer within the database'''
        if self.date < layer.startdate:
            self._db.updateTimeSeries(layer, startdate=self.date, commit=False)
        elif self.date > layer.enddate:
            self._db.updateTimeSeries(layer, enddate=self.date, commit=False)
        self.updateDatasetDates()
    
    def updateDatasetDates(self):
        '''Updates the datasets dates (self.dataset) within the database'''
        if self.dataset is None:
            self.dataset = self._db.getDatasets(filters={'id': self.dataset_id})
        if self.dataset.startdate is None or self.date < self.dataset.startdate:
            self._db.updateDatasetDates(self.dataset, startdate=self.date, commit=False)
        if self.dataset.enddate is None or self.date > self.dataset.enddate:
            self._db.updateDatasetDates(self.dataset, enddate=self.date, commit=False)
        
        
    def getExistingLayer(self):
        '''Returns duplicate if layer with same layertyoe already exists, false otherwise'''
        self.logger.info('Checking if layer with same layertype exists...')
        dupl = self._db.getRasterLayers(filters={'dataset_id': self.dataset_id, 'layertype': self.layertype})
        if len(dupl)==0:
            return None   
        else:
            self.logger.info('Layertype already exists...')
            return dupl[0]
        
        
        
    """def update(self, duplicate):
        '''Returns true if time layer should be updated, false otherwise'''
        self.logger.info('Checking for updates...')
        srcf = os.path.join(self.conf.getDataInputPath(), self.layerfile)
        timestamp = time.ctime(os.path.getmtime(srcf))
        timestamp = datetime.strptime(timestamp, "%a %b %d %H:%M:%S %Y")
        if timestamp >= duplicate.timestamp: 
            return True
        else:
            return False"""