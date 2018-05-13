'''

@author: livia
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from display_data.models import *
from definitions import CONFIG_PATH
import os
from configobj import ConfigObj
import shutil
import logging
from display_data.prepare_raster import RasterLayerProcessor, RasterTiler




class Query(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    def __repr__(self):
        return "this"
    




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
            self.Session.commit()
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
            self.Session.commit()
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
    
    
    def getLayers(self, ids=None):
        """returns a list of all requested datasets.
        
        Input parameter:
            ids – (optional) a list of integers or one single integer
                when ids is given only the requested datasets with matching ids are returned
                when ids is none every dataset is returned
        
        Returns:
            a list with Dataset objects/ one object
        
        """
        
        query = self.Session.query(Layer)
        
        if isinstance(ids, list):
            query=query.filter(Layer.id.in_(ids))
        elif isinstance(ids, int):
            query=query.filter(Layer.id == ids)
            
        return query.all()
    
    
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
        conf = ConfigSystem(dataset_id=dataset_id)
        conf.newLayerFolder(ltype)
        self.rollback.addCommand(conf.removeLayerFolder, {'ltype': ltype})
        layer = self._db.newLayer(dataset_id=dataset_id, layerTypeName=ltype, commit=False)
        
        print('ye')
        rast_proc = RasterLayerProcessor(layertype=ltype, logger=self.logger)
        print('ye2')
        fn, file_extension = os.path.splitext(filename) #extract extension
        print('ye2')
        srcf = os.path.join(conf.getDataInputPath(), filename)
        print('ye2')
        #save init file in output folder
        cp = os.path.join(conf.getLayerFolder(ltype, dataset_id), ('raw_input'+file_extension))
        shutil.copyfile(srcf, cp)
        
        # compute stats
        rast_proc.readFile(srcf)
        stats = rast_proc.getStatistics()
        print(stats)
        #scale = {'min': stats['min'], 'max': stats['max']}
        scale = {'min': -2, 'max': 2}
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
    
    
    
    
    
    def addDataset(self, layers, cite=None):
        print(self._db.Session)
        self._db.scopedSession()
        self.rollback.addCommand(self._db.closeSession)
        dataset = self._db.newDataset(cite, 1, commit=False)
        conf = ConfigSystem(dataset_id=dataset.id)
        conf.newDatasetFolder()
        self.rollback.addCommand(conf.removeDatasetFolder, {'d_id':dataset.id})
        
        print(dataset.id)
        
        print('test')
        for l in layers:
            self.addLayer(l[0], l[1], dataset.id)
        
        self._db.commit()
        self._db.closeSession()
        
        
        
        