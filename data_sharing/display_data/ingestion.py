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
        
        
    '''def addLayer(self, filename, ltype, dataset_id):
        
        print('Adding layer', filename)
        
        if self._db.Session is None:
            self._db.scopedSession()
            self.rollback.addCommand(self._db.closeSession)

        #check if entry already exist and if it should be updated
        self.logger.info('Checking if layer exists...')
        dupl = self._db.getRasterLayers(dataset_id=dataset_id, layertype_name=ltype)
        conf = ConfigSystem(dataset_id=dataset_id)
        if len(dupl)==0:
            conf.newLayerFolder(ltype)
            self.rollback.addCommand(conf.removeLayerFolder, {'ltype': ltype})
            layer = self._db.newRasterLayer(dataset_id=dataset_id, layerTypeName=ltype, commit=False)
            self.processRaster(filename=filename, ltype=ltype, dataset_id=dataset_id)
        else:
            srcf = os.path.join(conf.getDataInputPath(), filename)
            timestamp = time.ctime(os.path.getmtime(srcf))
            timestamp = datetime.strptime(timestamp, "%a %b %d %H:%M:%S %Y")
            print(type(timestamp),timestamp, type(dupl[0].timestamp), dupl[0].timestamp)
            if timestamp >= dupl[0].timestamp: ##update layer
                print('UPDATE LAYER....')
                self.processRaster(filename=filename, ltype=ltype, dataset_id=dataset_id)
                self._db.updateTimestamp(dupl[0], commit=False)
            else:
                msg = 'Layer with file={} , type={} datasetid={} is up to date.'.format(filename, ltype, dataset_id)
                self.logger.info(msg)
            ## check timestamps
            ## at the end update timestamp'''
    
    
    '''def processRaster(self, filename, ltype, dataset_id):
        conf = ConfigSystem(dataset_id=dataset_id)
        rast_proc = RasterLayerProcessor(logger=self.logger)
        file_extension = os.path.splitext(filename)[1] #extract extension
        srcf = os.path.join(conf.getDataInputPath(), filename)
        #save init file in output folder
        cp = os.path.join(conf.getLayerFolderByAttributes(ltype, dataset_id), (conf.getRawInputFilename()+file_extension))
        shutil.copyfile(srcf, cp)
        
        # compute stats
        rast_proc.readFile(srcf)
        stats = rast_proc.getStatistics()
        print(stats)
        #scale = {'min': stats['min'], 'max': stats['max']}
        
        #reproject
        proj = os.path.join(conf.getLayerFolderByAttributes(ltype, dataset_id), (conf.getReprojectedFilename()+file_extension))
        print("REPROJECT", proj)
        rast_proc.reproject(inputfile=srcf, outputfile=proj)
        
        #convert to 8bit
        #scale = conf.getLayerScale(ltype)
        #bit_8 = os.path.join(conf.getLayerFolderByAttributes(ltype, dataset_id), ('8bit'+file_extension))
        #rast_proc.to8Bit(inputfile=proj, outputfile=bit_8, scale=scale, exponent=conf.getExponent(layertype=ltype))
        
        ########### PRINT STATS
        #print(rast_proc.getStatistics())
        #rast_proc.readFile(bit_8)
        #print('EXPONENT: ', conf.getExponent(layertype=ltype))
        
        #cut raster
        cut = os.path.join(conf.getLayerFolderByAttributes(ltype, dataset_id), ('cropped'+file_extension))
        rast_proc.cutRaster(inputfile=proj, outputfile=cut)
        
        #compute colourfile
        col_inputfile = conf.getSampleColourFile(ltype)
        col_outputpath= os.path.join(conf.getLayerFolderByAttributes(ltype, dataset_id), ('colourfile.txt'))
        colgen = ColourMaker(col_inputfile, col_outputpath)
        scale = conf.getLayerScale(ltype)
        colgen.computeColours(scale['min'], scale['max'])
                
        #add colour
        col_rast = os.path.join(conf.getLayerFolderByAttributes(ltype, dataset_id), ('coloured'+file_extension))
        rast_proc.addColours(inputfile=cut, outputfile=col_rast, colourfile=col_outputpath) # take the above computed as input
        
        #TILEE
        tiler = RasterTiler()
        tiler.createTiles(col_rast, conf.getTilesFolder(ltype, d_id = dataset_id))
            
        print('FILE: ', filename, ' TYPE: ', ltype, ' DATASETID', dataset_id)'''
    
    
    
    '''def addLayerToDataset(self, filename, ltype, dataset_id):
        
        print('Adding layer', filename)
        
        if self._db.Session is None:
            self._db.scopedSession()
            self.rollback.addCommand(self._db.closeSession)
            
        self.addLayer(filename, ltype, dataset_id)   
            
        self.logger.info('Commit')  
        self._db.commit()
        self._db.closeSession()'''
    
    
    
    '''def addDataset(self, layers, cite=None):
        self._db.scopedSession()
        self.rollback.addCommand(self._db.closeSession)
        dataset = self._db.newDataset(cite, 1, commit=False)
        conf = ConfigSystem(dataset_id=dataset.id)
        conf.newDatasetFolder()
        self.rollback.addCommand(conf.removeDatasetFolder, {'d_id':dataset.id})
        
        self.addBoundingBox(dataset, layers)
        
        for l in layers:
            self.addLayer(l[0], l[1], dataset.id)
            
        self.logger.info('Commit...')
        self._db.commit()
        self._db.closeSession()
        
        
        
    def addBoundingBox(self, dataset, layers):
        assert len(layers) > 0
        ## for now just take the first layer
        file_extension = os.path.splitext(layers[0][0])[1]
        conf = ConfigSystem(dataset_id=dataset.id)
        srcf = os.path.join(conf.getDataInputPath(), layers[0][0])
        rast_proc = RasterLayerProcessor(self.logger)
        
        repr_file = 'reproject.'+file_extension
        repr_filepath = os.path.join(conf.getDataInputPath(), repr_file)
        rast_proc.reproject(srcf, repr_filepath)
        print('reprojected')
        rast_proc.readFile(repr_filepath)
        print(rast_proc.getProjection())
        box=rast_proc.getMinBoundingBox()        
        dataset.xmin = box['xmin']
        dataset.xmax = box['xmax']
        dataset.ymin = box['ymin']
        dataset.ymax = box['ymax']
        os.remove(repr_filepath)
        self.logger.info('ADDED BOUNDING BOX')'''
        
        
        
        








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
        self.rollback.addCommand(self.conf.removeDatasetFolder, {'d_id':dataset.id})
        
        self.addBoundingBox(dataset)
        self.addArea(dataset)
        
        # create layers
        for l in self.layers:
            l['dataset_id'] = dataset.id
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
        
        print('DATE' , self.date, type(self.date))
        
        self.conf = ConfigSystem(dataset_id=self.dataset_id)
        self.layerfolder = self.conf.getLayerFolderByAttributes(self.layertype, self.date, self.dataset_id)
        scale = self.conf.getLayerScale(self.layertype)
        if 'min' in kwargs:
            self.min = kwargs['min']
        else:
            self.min = scale['min']
            
        if 'max' in kwargs:
            self.max = kwargs['max']
        else:
            self.max = scale['max']
     
     
     
                
        
    
    def create(self):
        '''Creates the raster layer'''        
        duplicate = self.getDuplicate()
        
        print('DUPLICTAE',duplicate)
        
        if duplicate is None:
            # insert into database
            layer = self._db.newRasterLayer(dataset_id=self.dataset_id, layerType=self.layertype, date=self.date, commit=False)
            #process raster
            self.conf.newLayerFolder(layer)
            self.rollback.addCommand(self.conf.removeLayerFolder, {'layer': layer})
            
            self.processFile()
        elif self.update(duplicate):
            self.processFile()
            self._db.updateTimestamp(duplicate, commit=False)
        else:
            msg = 'Layer with file={} , type={} datasetid={} is up to date.'.format(self.layerfile, self.layertype, self.dataset_id)
            self.logger.info(msg)
        
        
        
    def processFile(self):
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
        cp = os.path.join(self.layerfolder, (self.conf.getRawInputFilename()+file_extension))
        shutil.copyfile(srcf, cp)
        
        # 2. reproject
        proj = os.path.join(self.layerfolder, (self.conf.getReprojectedFilename()+file_extension))
        self.rast_proc.reproject(inputfile=srcf, outputfile=proj)
        
        # 3. cut raster
        cut = os.path.join(self.layerfolder, ('cropped'+file_extension))
        self.rast_proc.cutRaster(inputfile=proj, outputfile=cut)
        
        # 4. compute colourfile
        col_inputfile = self.conf.getSampleColourFile(self.layertype)
        col_outputpath= os.path.join(self.layerfolder, ('colourfile.txt'))
        colgen = ColourMaker(col_inputfile, col_outputpath)
        colgen.computeColours(self.min, self.max)
                
        # 5. add colour
        col_rast = os.path.join(self.conf.getLayerFolderByAttributes(self.layertype, self.date, self.dataset_id), ('coloured'+file_extension))
        self.rast_proc.addColours(inputfile=cut, outputfile=col_rast, colourfile=col_outputpath) # take the above computed as input
        
        # 6. tile
        tiler = RasterTiler()
        tiler.createTiles(col_rast, self.conf.getTilesFolder(self.layertype, self.date, d_id = self.dataset_id))
            
        print('FILE: ', self.layerfile, ' TYPE: ', self.layertype, ' DATASETID', self.dataset_id)
        
    
    
    def getDuplicate(self):
        '''Returns true if layer already exists, false otherwise'''
        self.logger.info('Checking if layer exists...')
        dupl = self._db.getRasterLayers(filters={'dataset_id': self.dataset_id, 'layertype': self.layertype, 'date': self.date})
        if len(dupl)==0:
            return None   
        else:
            self.logger.info('Duplicate discovered...')
            return dupl[0]
        
        
    def update(self, duplicate):
        '''Returns true if layer should be updated, false otherwise'''
        self.logger.info('Checking for updates...')
        srcf = os.path.join(self.conf.getDataInputPath(), self.layerfile)
        timestamp = time.ctime(os.path.getmtime(srcf))
        timestamp = datetime.strptime(timestamp, "%a %b %d %H:%M:%S %Y")
        print(type(timestamp),timestamp, type(duplicate.timestamp), duplicate.timestamp)
        if timestamp >= duplicate.timestamp: 
            return True
        else:
            return False