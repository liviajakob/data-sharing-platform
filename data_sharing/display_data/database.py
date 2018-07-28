'''Manages creation, ingestion and querying of database

Contains:
    Database

@author: livia
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from display_data.models import * # import all the models
import os
from display_data.system_configuration import ConfigSystem
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime



class Database():
    

    def __init__(self, dbSettings={}, logger=None, rollback=None, echo=False):
        '''
        Input Parameter:
            dbSettings - dictionary containing:
                        'type' : type of db (e.g. sqllite, or oracle, or mysql)
                        'path' : path to database
                        'name' : database name
            logger – a loging object
            rollback – a Rollback object
            echo (boolean) – determines if database queries are printed in console
                    
        '''
        
        if len(dbSettings)==0:
            filesys = ConfigSystem()
            self._engine = create_engine(filesys.dbEngine()+filesys.dbPath(), echo=echo)  
        else:
            self._engine = create_engine(dbSettings['type']+os.path.join(dbSettings['path'],dbSettings['name']), echo=echo)

        self.rollback = rollback
        self.logger = logger
        self.conf = ConfigSystem()
        
        self.Session = None #capital because it's a factory
        createModels(self._engine)

        
    def createTables(self):
        '''Creates database structure from Models in models.py'''
        createModels(self._engine)
    
    
    def scopedSession(self):
        '''Creates a scoped session'''
        self.Session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=self._engine))
    
    def closeSession(self):
        '''Closes the current session'''
        assert self.Session != None #Check connection open
        self.Session.close()
        self.Session=None
    
    
    def commit(self):
        '''Commit the current session'''
        self.Session.commit()
    
    def newDataset(self, cite, projection, commit=True):
        """Adds a new dataset to the database
        
        Input Parameter:
            cite (str) – how to cite the dataset
            projection (str) – A projection code
            commit (boolean) – default: True, determines if session should commit
        
        """  
        assert self.Session is not None
        
        if cite is None:
            cite="No information given."
            
        try:
            dataset = Dataset()
            dataset.cite = cite
            dataset.projection=projection #add foreign key
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
        except SQLAlchemyError:
            self.Session.rollback()
            raise SQLAlchemyError
            
            
        
    def newRasterLayerGroup(self, dataset_id, layerType, date, commit=True):
        """Adds a new raster layergroup to a dataset
        
        Input Parameter:
            dataset_id (int) – ID of corresponding dataset
            layerType (str) – type of layer, e.g. dem
            date (datetime.date) – a python dat object
            commit (boolean) – default: True, determines if session should commit
        
        """        
        try:
            dataset = self.Session.query(Dataset).filter(Dataset.id==dataset_id).one() 
        except SQLAlchemyError as e:
            self.logger.error("input '{}' is NO valid dataset id".format(dataset_id))
            raise e
        
        try:
            layergr = RasterLayerGroup()
            layergr.dataset_id = dataset.id
            layergr.layertype = layerType
            layergr.startdate = date
            layergr.enddate = date
            
            self.Session.add(layergr)
            if commit:
                self.Session.commit()
            else:
                self.Session.flush()
                return layergr
        except SQLAlchemyError as e:
            self.Session.rollback()
            raise e
       
        
        
    def dropTables(self):
        '''Drops all tables within the database, used for testing
        
        '''
        assert self.Session is not None
        Base.metadata.drop_all(self._engine) #drop all tables

        
        
    def getTableNames(self):
        '''Returns a list with database table names
        '''
        return self._engine.table_names()
        
        
    def getDatasets(self, filters={}, dic=False, page=None, page_size=None, orderbyarea=False, layerinfo=False):
        """returns a list of all requested datasets.
        
        Input parameter:
            filters – (optional) a dictionary of filter statements
            dic - (default: False) if dic is set true it will return a dictionary
            page (int) - (optional) page number to be queried
            page_size (int) – (optional) page size to be queried
            orderbyarea - True if results should be ordered by area (descending; largest datasets first)
            layerinfo (boolean) – (default: False) if True detailed info on layers is given
            
        Returns:
            a list with Dataset objects/ one object OR a dictionnary
        
        """
        query = self.Session.query(Dataset)
        
        #add filters
        for attr, value in filters.items():
            if hasattr(Dataset, attr):
                if attr == "startdate":
                    value = datetime.strptime(filters[attr], "%Y-%m-%d")
                    query = query.filter(value >= getattr(Dataset, 'startdate'))
                elif attr == "enddate":
                    value = datetime.strptime(filters[attr], "%Y-%m-%d")
                    query = query.filter(value <= getattr(Dataset, 'enddate'))
                else: 
                    query = query.filter(getattr(Dataset, attr) == value)
            elif hasattr(RasterLayerGroup, attr): #filter to join tables
                query=query.outerjoin(RasterLayerGroup).filter(getattr(RasterLayerGroup, attr) == value).filter(RasterLayerGroup.dataset_id == Dataset.id)

        if page_size:
            query = query.limit(page_size)
            
        if page: 
            query = query.offset(page*page_size)

        if not dic:
            try:
                result=query.all()   
                if orderbyarea:
                    result.sort(key=lambda x: x.area, reverse=True)
                return result
            except SQLAlchemyError:
                return []
        else: 
            try:
                result=query.all() 
                if orderbyarea:
                    result.sort(key=lambda x: x.area, reverse=True)
                return self.asDictionary(result, layerinfo=layerinfo) 
            except SQLAlchemyError:
                geoCollection = {}
                geoCollection['type']= 'FeatureCollection'
                geoCollection['features'] = []
                return geoCollection
    

    
    
    def getRasterLayerGroups(self, filters={}):
        """returns a list of all requested datasets.
        
        Input parameter:
            filters – (optional) a list of filteroptions
                e.g. filters={'dataset_id' : 1, 'layertype' : 'dem'}
                
        Returns:
            a list with Dataset objects/ one object or a dictionnary
        
        """

        query = self.Session.query(RasterLayerGroup)
        
        for attr, value in filters.items():
            query = query.filter(getattr(RasterLayerGroup, attr) == value)
        
        try:
            return query.all()
        except SQLAlchemyError:
            return []
    
    
    def getLayerGroups(self, filters={}):
        """returns a list of all requested layer groups.
        
        Input parameter:
            filters – (optional) a list of filteroptions
                e.g. filters={'dataset_id' : 1, 'layertype' : 'dem'}
            dic – true if result should be returned as dictionnary
                
        Returns:
            a list with layergroup objects/ one object or a dictionnary, sorted on layertype
        
        """
        # we only have Raster Layer Groups for now...
        result = self.getRasterLayerGroups(filters=filters)
        result.sort(key=lambda x: x.layertype, reverse=False)
        ## if pointlayer in database they would be added here to the result
        return result
    
    
    
    
    def asDictionary(self, datasets, layerinfo=False):
        '''Returns a list of datasets as dictionary in GeoJSON format
        
        Input Parameter:
            datasets – a list of Dataset objects
            layerinfo (boolean) – (default: False) if True detailed info on layers is given
        
        '''
        features=[]
        for ds in datasets:
            geodic = ds.asGeoDict()
            layergr = self.getLayerGroups({'dataset_id' : ds.id})
            layers_dict=[]
            for l in layergr:
                l_dict=l.asDict()
                if layerinfo:
                    l_dict['layers'] = self.getLayerDict(l)
                layers_dict.append(l_dict)
                
            geodic['properties']['layergroups'] = layers_dict
            features.append(geodic)
        geoCollection = {}
        geoCollection['type']= 'FeatureCollection'
        geoCollection['features'] = features
    
        return geoCollection
    
   
    def getLayerDict(self, layergroup):
        '''Returns the layers as dictionary
        
        Input Parameter:
            layergroup - a RasterLayerGroup object
            
        '''
        layers = []
        dates = self.conf.getLayerDates(layergroup)
        for val in reversed(dates):
            tile = self.conf.getRelativeTilesFolder(layergroup, val)
            layers.append({'date': val, 'tileurl': tile})
        return layers
    

            
    def updateLayerGroupDates(self, layergroup, startdate=None, enddate=None, commit=True):
        '''Updates a layergroups start or enddate if the new date is not within the old timespan
        
        Input Parameter:
            layergroup – a Layergroup/RasterLayerGroup object
            startdate (datetime.date) – (optional) date to be checked
            enddate (datetime.date) – (optinal) date to be checked
            commit (boolean) – (default: False), determines if session should commit
        
        
        '''
        assert self.Session is not None
        if enddate is not None:
            layergroup.enddate = enddate
        if startdate is not None:
            layergroup.startdate = startdate
        if commit:
            self.Session.commit()
        else:
            self.Session.flush()
        

            
    def updateDatasetDates(self, dataset, startdate=None, enddate=None, commit=True):
        '''Updates a datasets start or enddate if the new date is not within the old timespan
        
                
        Input Parameter:
            dataset – a Dataset object
            startdate (datetime.date) – (optional) date to be checked
            enddate (datetime.date) – (optinal) date to be checked
            commit (boolean) – (default: False), determines if session should commit
        
        
        '''
        assert self.Session is not None
        if enddate is not None:
            dataset.enddate = enddate
        if startdate is not None:
            dataset.startdate = startdate
        if commit:
            self.Session.commit()
        else:
            self.Session.flush()
    