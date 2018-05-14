'''

@author: livia
'''

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, scoped_session
from display_data.models import *
from definitions import CONFIG_PATH
import os, time
from configobj import ConfigObj
import shutil
import logging
from display_data.prepare_raster import RasterLayerProcessor, RasterTiler
from datetime import datetime
from display_data.system_configuration import ConfigSystem




class Database():
    

    def __init__(self, dbSettings={}, rollback=None):
        '''
        
        Input Parameter:
            dbSettings - dictionary containing:
                        'type' : type of db (e.g. sqllite, or oracle, or mysql)
                        'path' : path to database
                        'name' : database name
                    
        '''
        
        if len(dbSettings)==0:
            filesys = ConfigSystem()
            self._engine = create_engine(filesys.dbEngine()+filesys.dbPath(), echo=False)

            
        else:
            # @TODO: more tests
            self._engine = create_engine(dbSettings['type']+os.path.join(dbSettings['path'],dbSettings['name']), echo=True)


        
        #self._engine = create_engine(self._db['type']+os.path.join(self._db['path'],self._db['name']), echo=True)
        #Base.metadata.create_all(bind=engine)
        #Session = sessionmaker(bind=engine)
        
        self.Session = None #capital because it's a factory
        createModels(self._engine)

        
        #session=Session()
        
    def createTables(self):
        createModels(self._engine)
    
    
    def scopedSession(self):
        self.Session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=self._engine))
    
    def closeSession(self):
        assert self.Session != None #Check connection open
        self.Session.close()
        #self.Session=None
    
    
    def commit(self):
        self.Session.commit()
    
    def newDataset(self, cite, projection_id, commit=True):
        """Adds a new dataset to the database
        
        
        """
        assert self.Session is not None
        
        try:
            proj = self.Session.query(Projection).filter(Projection.id==projection_id).one() 
        except:
            print("NO valid projection")
            raise
            
        try:
            dataset = Dataset()
            dataset.cite = cite
            dataset.projection_id=proj.id #add foreign key
            dataset.xmin = None
            dataset.xmax = None
            dataset.ymin = None
            dataset.ymax = None
            self.Session.add(dataset)
            #commit
            if commit:
                self.Session.commit()
            else:
                self.Session.flush()
                return dataset
        except:
            self.Session.rollback()
            raise
            
            
        
    def newProjection(self, name, commit=True):
        """Adds a new projection to the database"""
        assert self.Session is not None
        
        try:
            projection = Projection()
            projection.name = name
            self.Session.add(projection)
            if commit:
                self.Session.commit()
            else:
                self.Session.flush()
        except:
            self.Session.rollback()
            raise
        
    def newLayer(self, dataset_id, layerTypeName, commit=True):
        """Adds a new dataset layer to a data set"""
        
        try:
            layerType = self.Session.query(LayerType).filter(LayerType.name==layerTypeName).one() 
        except:
            print("input '{}' is NO valid layertype".format(layerTypeName))
            raise
        
        try:
            dataset = self.Session.query(Dataset).filter(Dataset.id==dataset_id).one() 
        except:
            print("input '{}' is NO valid is NO valid dataset id".format(dataset_id))
            raise
        
        try:
            layer = Layer()
            layer.type_id = layerType.id
            layer.dataset_id = dataset.id
            layer.layertype_id = layerType.id
            self.Session.add(layer)
            if commit:
                self.Session.commit()
            else:
                self.Session.flush()
                return layer
        except:
            self.Session.rollback()
            raise
       
        
    def newLayerType(self, name, commit=True):
        
        assert self.Session is not None
        
        try:
            layerType = LayerType()
            layerType.name = name
            self.Session.add(layerType)
            self.Session.commit()
            if commit:
                self.Session.commit()
            else:
                self.Session.flush()
        except:
            self.Session.rollback()
            raise
        
        
        
        
    def dropTables(self, pw=None):
        '''
        Drops all tables within the database, used for testing
        '''
        assert self.Session is not None
        
        if pw =="livia":
            Base.metadata.drop_all(self._engine) #drop all tables
        else:
            print("No access to drop tables")
        
        
    def getTableNames(self):
        '''returns a list with table names
        '''
        return self._engine.table_names()
        
        
    def getDatasets(self, ids=None):
        """returns a list of all requested datasets.
        
        Input parameter:
            ids – (optional) a list of integers or one single integer
                when ids is given only the requested datasets with matching ids are returned
                when ids is none every dataset is returned
        
        Returns:
            a list with Dataset objects/ one object
        
        """
        
        query = self.Session.query(Dataset)
        
        if isinstance(ids, list):
            query=query.filter(Dataset.id.in_(ids))
        elif isinstance(ids, int):
            query=query.filter(Dataset.id == ids)
            
        return query.all()
    
    def getLayertypeByName(self, tname):
        query = self.Session.query(LayerType)
        query=query.filter(LayerType.name == tname)
        try:
            return query.first()
        except Exception as e:
            print (e)
            return []    
    
    def getLayerById(self, l_id):

        query = self.Session.query(Layer)
        query=query.filter(Layer.id == l_id)
        try:
            return query.all()
        except Exception as e:
            print (e)
            print('query all')
            return []    
        
    
    
    
    def getLayerByAttributes(self, dataset_id=None, layertype_name=None):
        """returns a list of all requested datasets.
        
        Input parameter:
            ids – (optional) a list of integers or one single integer
                when ids is given only the requested datasets with matching ids are returned
                when ids is none every dataset is returned
        
        Returns:
            a list with Dataset objects/ one object
        
        """
        
        print('get Layer')
        l_typeid = self.getLayertypeByName(layertype_name)
        print(l_typeid)
        print(type(l_typeid))
        query = self.Session.query(Layer)
        print('datasetid',dataset_id)
        print(l_typeid.id)
        query=query.filter(and_(Layer.dataset_id == dataset_id, Layer.layertype_id == l_typeid.id))
        print('eh2')
        try:
            print('qur')
            print(query)
            print(query.all(), type(query.all()))
            print('qu2')
            return query.all()
        except Exception as e:
            print (e)
            print('query all')
            return []    
        
    
    
    def getLayerTypes(self, ids=None):
        """returns a list of all requested datasets.
        
        Input parameter:
            ids – (optional) a list of integers or one single integer
                when ids is given only the requested datasets with matching ids are returned
                when ids is none every dataset is returned
        
        Returns:
            a list with Dataset objects/ one object
        
        """
        
        query = self.Session.query(LayerType)
        
        if isinstance(ids, list):
            query=query.filter(LayerType.id.in_(ids))
        elif isinstance(ids, int):
            query=query.filter(LayerType.id == ids)
            
        return query.all()
    
    
    def getProjections(self, ids=None):
        """returns a list of all requested projections.
        
        Input parameter:
            ids – (optional) a list of integers or one single integer
                when ids is given only the requested projections with matching ids are returned
                when ids is none every projection is returned
        
        Returns:
            a list with Projection objects
        
        """
        
        query = self.Session.query(Projection)
        
        if isinstance(ids, list):
            query=query.filter(Dataset.id.in_(ids))
        elif isinstance(ids, int):
            query=query.filter(Dataset.id == ids)
            
        return query.all()
    

    def updateTimestamp(self, layer, commit=True):
        
        assert self.Session is not None
        
        time = datetime.utcnow() 
        
        layer.timestamp = time
        if commit:
            self.Session.commit()
        else:
            self.Session.flush()
        
        
        




    
    
    

    
    
    
    
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
        print(dupl)
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
                print('UPDATE LAYER')
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
    
    
    
    def addOneLayer(self, filename, ltype, dataset_id):
        
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
            
        print('commit')
        self._db.commit()
        self._db.closeSession()
        
        
        
    def addBoundingBox(self, dataset, layers):
        assert len(layers) > 0
        ## for now just take the first layer
        
        conf = ConfigSystem(dataset_id=dataset.id)
        srcf = os.path.join(conf.getDataInputPath(), layers[0][0])
        rast_proc = RasterLayerProcessor(self.logger)
        rast_proc.readFile(srcf)
        box=rast_proc.getBoundingBox()        
        dataset.xmin = box['xmin']
        dataset.xmax = box['xmax']
        dataset.ymin = box['ymin']
        dataset.ymax = box['ymax']
        self.logger.info('ADDED BOUNDING BOX')
        
        
        