'''

@author: livia
'''

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, scoped_session
from display_data.models import *
import os
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
        
        if cite is None:
            cite="No information given."
        
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
        l_typeid = self.getLayertypeByName(layertype_name)
        print(type(l_typeid))
        query = self.Session.query(Layer)
        print('datasetid ',dataset_id)
        print(l_typeid.id)
        query=query.filter(and_(Layer.dataset_id == dataset_id, Layer.layertype_id == l_typeid.id))
        try:
            return query.all()
        except Exception as e:
            print (e)
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
        
