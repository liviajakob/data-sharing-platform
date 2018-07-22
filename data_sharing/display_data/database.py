'''

@author: livia
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from display_data.models import *
import os
from display_data.system_configuration import ConfigSystem
from numpy.lib.tests.test_io import strptime




class Database():
    

    def __init__(self, dbSettings={}, logger=None, rollback=None, echo=False):
        '''
        
        Input Parameter:
            dbSettings - dictionary containing:
                        'type' : type of db (e.g. sqllite, or oracle, or mysql)
                        'path' : path to database
                        'name' : database name
            echo - determines if database operations are printed in console
                    
        '''
        
        if len(dbSettings)==0:
            filesys = ConfigSystem()
            self._engine = create_engine(filesys.dbEngine()+filesys.dbPath(), echo=echo)

            
        else:
            # @TODO: more tests
            self._engine = create_engine(dbSettings['type']+os.path.join(dbSettings['path'],dbSettings['name']), echo=echo)

        self.rollback = rollback
        self.logger = logger
        self.conf = ConfigSystem()

        
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
    
    def newDataset(self, cite, projection, commit=True):
        """Adds a new dataset to the database
        
        
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
        except:
            self.Session.rollback()
            raise
            
            
        
    def newRasterLayerGroup(self, dataset_id, layerType, date, commit=True):
        """Adds a new dataset layergr to a data set"""        
        try:
            dataset = self.Session.query(Dataset).filter(Dataset.id==dataset_id).one() 
        except Exception as e:
            self.logger.error("input '{}' is NO valid is NO valid dataset id".format(dataset_id))
            raise e
        
        try:
            layergr = RasterLayerGroup()
            #layergr.type_id = layerType.id
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
        '''Returns a list with database table names
        '''
        return self._engine.table_names()
        
        
    def getDatasets(self, filters={}, dic=False, page=None, page_size=None, orderbyarea=False, layerinfo=False):
        """returns a list of all requested datasets.
        
        Input parameter:
            filters – (optional) a list of filter statements
            dic - (default: True) if dic is set true it will return a dictionnary which can be converted to a geojson
            orderbyarea - True if results should be ordered by area (descending; largest datasets first)
            
        Returns:
            a list with Dataset objects/ one object OR a dictionnary
        
        """
        query = self.Session.query(Dataset)
        
        #add filters
        for attr, value in filters.items():
            if hasattr(Dataset, attr):
                if attr == "startdate":
                    value = strptime(filters[attr], "%Y-%m-%d")
                    query = query.filter(value >= getattr(Dataset, 'startdate'))
                elif attr == "enddate":
                    value = strptime(filters[attr], "%Y-%m-%d")
                    query = query.filter(value <= getattr(Dataset, 'enddate'))
                else: 
                    query = query.filter(getattr(Dataset, attr) == value)
            elif hasattr(RasterLayerGroup, attr): #filter to join tables
                query=query.outerjoin(RasterLayerGroup).filter(getattr(RasterLayerGroup, attr) == value).filter(RasterLayerGroup.dataset_id == Dataset.id)

        if page_size:
            query = query.limit(page_size)
            
        if page: 
            query = query.offset(page*page_size)
    
        
        print('dic', dic)
        if not dic:
            try:
                result=query.all()   
                if orderbyarea:
                    result.sort(key=lambda x: x.area, reverse=True)
                print('result ', result)
                return result
            except:
                return []
        else: 
            try:
                result=query.all() 
                if orderbyarea:
                    result.sort(key=lambda x: x.area, reverse=True)
                print('geoCollection ', self.asDictionary(result, layerinfo=layerinfo))
                return self.asDictionary(result, layerinfo=layerinfo) 
            except Exception as e:
                print('Exception ',e)
                print('No results found')
                geoCollection = {}
                geoCollection['type']= 'FeatureCollection'
                geoCollection['features'] = []
                return geoCollection
    

    
    
    def getRasterLayerGroups(self, filters={}):
        """returns a list of all requested datasets.
        
        Input parameter:
            filters – (optional) a list of filteroptions
                e.g. filters={'dataset_id' : 1, 'layertype' : 'dem'}
            dic – true if result should be returned as dictionnary
                
        Returns:
            a list with Dataset objects/ one object or a dictionnary
        
        """

        query = self.Session.query(RasterLayerGroup)
        
        for attr, value in filters.items():
            query = query.filter(getattr(RasterLayerGroup, attr) == value)
        
        #query=query.filter(filterrule)
        try:
            return query.all()
        except Exception as e:
            #print (e)
            return []
    
    
    def getLayerGroups(self, filters={}):
        """returns a list of all requested layer groups.
        
        Input parameter:
            filters – (optional) a list of filteroptions
                e.g. filters={'dataset_id' : 1, 'layertype' : 'dem'}
            dic – true if result should be returned as dictionnary
                
        Returns:
            a list with layergroup objects/ one object or a dictionnary
        
        """
        # we only have Raster Layer Groups for now...
        result = self.getRasterLayerGroups(filters=filters)
        result.sort(key=lambda x: x.layertype, reverse=False)
        ## if pointlayer in database they would be added here to the result
        return result
    
    
    
    
    def asDictionary(self, datasets, layerinfo=False):
        '''Returns a list of datasets as dictionary in GeoJSON format'''
        features=[]
        for ds in datasets:
            geodic = ds.asGeoDict()
            layergr = self.getLayerGroups({'dataset_id' : ds.id})
            layers_dict=[]
            for l in layergr:
                l_dict=l.asDict()
                #tile_url = self.conf.getRelativeTilesFolder(l)
                #l_dict['tileurl'] = tile_url
                if layerinfo:
                    l_dict['layers'] = self.getLayerDict(l)
                #l_dict['layertype']=self.getLayertypeById(l.layertype).name
                layers_dict.append(l_dict)
                
            geodic['properties']['layergroups'] = layers_dict
            features.append(geodic)
            
        #print(geoDict)
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
        '''Updates a layers start if the new time layergroup is not within the old time span'''
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
        '''Updates a layers start if the new time layer is not within the old time span'''
        assert self.Session is not None
        if enddate is not None:
            dataset.enddate = enddate
        if startdate is not None:
            dataset.startdate = startdate
        if commit:
            self.Session.commit()
        else:
            self.Session.flush()
    