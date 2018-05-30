'''

@author: livia
'''

import os, time
import shutil
from display_data.prepare_raster import RasterLayerProcessor, RasterTiler
from datetime import datetime
from display_data.system_configuration import ConfigSystem
from display_data.database import Database

    
    
class DatabaseIngestion(object):
    '''Handles everything to ingest an new entry'''
    
    def __init__(self, rollback, logger, database=None):
        if database is None:
            self._db = Database(rollback=rollback) #use the standard settings from the config file
        else:
            self._db = database
        
        self.rollback = rollback
        self.logger=logger
        
        
        
    def addLayer(self, filename, ltype, dataset_id):
        
        print('Adding layer', filename)
        
        if self._db.Session is None:
            self._db.scopedSession()
            self.rollback.addCommand(self._db.closeSession)

        #check if entry already exist and if it should be updated
        self.logger.info('Checking if layer exists...')
        dupl = self._db.getLayerByAttributes(dataset_id=dataset_id, layertype_name=ltype)
        conf = ConfigSystem(dataset_id=dataset_id)
        if len(dupl)==0:
            conf.newLayerFolder(ltype)
            self.rollback.addCommand(conf.removeLayerFolder, {'ltype': ltype})
            layer = self._db.newLayer(dataset_id=dataset_id, layerTypeName=ltype, commit=False)
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
            ## at the end update timestamp
    
    
    def processRaster(self, filename, ltype, dataset_id):
        conf = ConfigSystem(dataset_id=dataset_id)
        rast_proc = RasterLayerProcessor(logger=self.logger)
        fn, file_extension = os.path.splitext(filename) #extract extension
        srcf = os.path.join(conf.getDataInputPath(), filename)
        #save init file in output folder
        cp = os.path.join(conf.getLayerFolder(ltype, dataset_id), ('raw_input'+file_extension))
        shutil.copyfile(srcf, cp)
        
        # compute stats
        rast_proc.readFile(srcf)
        stats = rast_proc.getStatistics()
        print(stats)
        #scale = {'min': stats['min'], 'max': stats['max']}
        scale = conf.getLayerScale(ltype)
        bit_8 = os.path.join(conf.getLayerFolder(ltype, dataset_id), ('8bit'+file_extension))
        rast_proc.to8Bit(inputfile=srcf, outputfile=bit_8, scale=scale, exponent=conf.getExponent(layertype=ltype))
        
        ########### PRINT STATS
        rast_proc.readFile(bit_8)
        print('EXPONENT: ', conf.getExponent(layertype=ltype))
        print(rast_proc.getStatistics())
        
        #cut raster
        cut = os.path.join(conf.getLayerFolder(ltype, dataset_id), ('cropped'+file_extension))
        rast_proc.cutRaster(inputfile=bit_8, outputfile=cut)        
        #add colour
        col_rast = os.path.join(conf.getLayerFolder(ltype, dataset_id), ('coloured'+file_extension))
        colourfile = conf.getColourFile(ltype)
        rast_proc.addColours(inputfile=cut, outputfile=col_rast, colourfile=colourfile) # take the above computed as input
        
        #TILLEE
        tiler = RasterTiler()
        tiler.createTiles(col_rast, conf.getTilesFolder(ltype, d_id = dataset_id))
            
        print('FILE: ', filename, ' TYPE: ', ltype, ' DATASETID', dataset_id)
    
    
    
    def addLayerToDataset(self, filename, ltype, dataset_id):
        
        print('Adding layer', filename)
        
        if self._db.Session is None:
            self._db.scopedSession()
            self.rollback.addCommand(self._db.closeSession)
            
        self.addLayer(filename, ltype, dataset_id)   
            
        self.logger.info('Commit')  
        self._db.commit()
        self._db.closeSession()
    
    
    
    def addDataset(self, layers, cite=None):
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
        
        conf = ConfigSystem(dataset_id=dataset.id)
        srcf = os.path.join(conf.getDataInputPath(), layers[0][0])
        rast_proc = RasterLayerProcessor(self.logger)
        rast_proc.readFile(srcf)
        box=rast_proc.getMinBoundingBox()        
        dataset.xmin = box['xmin']
        dataset.xmax = box['xmax']
        dataset.ymin = box['ymin']
        dataset.ymax = box['ymax']
        self.logger.info('ADDED BOUNDING BOX')
        
        
        