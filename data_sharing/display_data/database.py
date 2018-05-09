'''

@author: livia
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from display_data.models import *
from definitions import CONFIG_PATH
import os
from configobj import ConfigObj


config = ConfigObj(CONFIG_PATH)


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
    

    def __init__(self, dbSettings={}):
        '''
        
        Input Parameter:
            dbSettings - dictionary containing:
                        'type' : type of db (e.g. sqllite, or oracle, or mysql)
                        'path' : path to database
                        'name' : database name
                    
        '''
        
        if len(dbSettings)==0:
            self._db = config['db']
        else:
            # @TODO: more tests
            self._db = dbSettings

        
        self._engine = create_engine(self._db['type']+os.path.join(self._db['path'],self._db['name']), echo=True)
        #Base.metadata.create_all(bind=engine)
        #Session = sessionmaker(bind=engine)
        
        self.Session = None #capital because it's a factory
        createModels(self._engine)

        
        #session=Session()
        
    
    
    def scopedSession(self):
        self.Session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=self._engine))
    
    def closeSession(self):
        assert self.Session != None #Check connection open
        self.Session.close()
        #self.Session=None
    
    def newDataset(self, name, cite, projection_id):
        """Adds a new dataset to the database
        
        
        """
        
        try:
            proj = self.Session.query(Projection).filter(Projection.id==projection_id).one() 
        except:
            print("NO valid projection")
            raise
            
        try:
            dataset = Dataset()
            dataset.name= name
            dataset.cite = cite
            dataset.projection_id=proj.id #add foreign key
            self.Session.add(dataset)
            #commit
            self.Session.commit()
        except:
            self.Session.rollback()
            raise
            
            
        
    def newProjection(self, name):
        """Adds a new projection to the database"""
        
        try:
            projection = Projection()
            projection.name = name
            self.Session.add(projection)
            self.Session.commit()
        except:
            self.Session.rollback()
            raise
        
    def newLayer(self, dataset_id, layerTypeName):
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
        except:
            self.Session.rollback()
            raise
       
        
    def newLayerType(self, name):
        
        try:
            layerType = LayerType()
            layerType.name = name
            self.Session.add(layerType)
            self.Session.commit()
        except:
            self.Session.rollback()
            raise
        
        
        
        
    def dropTables(self, pw=None):
        '''
        Drops all tables within the database, used for testing
        '''
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
    
 
 
    
    
class DatabaseIngestion(object):
    '''Handles everything to ingest an new entry'''
    
    def __init__(self, inputfile):
        self._database = Database() #use the standard settings from the config file
        
        
    def addLayer(self):
        pass