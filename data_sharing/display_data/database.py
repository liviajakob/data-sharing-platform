'''

@author: livia
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from display_data.models import *
import os
from datetime import datetime
from display_data.system_configuration import ConfigSystem
from numpy.lib.tests.test_io import strptime
from pandas.util.testing import getTimeSeriesData




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
        
        """try:
            proj = self.Session.query(Projection).filter(Projection.id==projection).one() 
        except:
            print("NO valid projection")
            raise"""
            
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
            
            
        
    def newRasterLayer(self, dataset_id, layerType, date, commit=True):
        """Adds a new dataset layer to a data set"""        
        try:
            dataset = self.Session.query(Dataset).filter(Dataset.id==dataset_id).one() 
        except Exception as e:
            self.logger.error("input '{}' is NO valid is NO valid dataset id".format(dataset_id))
            raise e
        
        try:
            layer = RasterLayer()
            #layer.type_id = layerType.id
            layer.dataset_id = dataset.id
            layer.layertype = layerType
            layer.startdate = date
            layer.enddate = date
            
            self.Session.add(layer)
            if commit:
                self.Session.commit()
            else:
                self.Session.flush()
                return layer
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
        
        
    def getDatasets(self, filters={}, dic=False, page=None, page_size=None, orderbyarea=False, timelayers=False):
        """returns a list of all requested datasets.
        
        Input parameter:
            filters – (optional) a list of filter statements
            dic - (default: True) if dic is set true it will return a dictionnary which can be converted to a geojson
            orderbyarea - True if results should be ordered by area (descending; largest datasets first)
            
        Returns:
            a list with Dataset objects/ one object OR a dictionnary
        
        """
        query = self.Session.query(Dataset)
        
        print('FILETRS', filters)
        
        #calculate time period
        if 'startdate' in filters or 'enddate' in filters:
            print(filters['startdate'])
            value = strptime(filters['startdate'], "%Y-%m-%d")
            print(value)
            query=query.outerjoin(RasterLayer).filter(getattr(RasterLayer, 'startdate') <= value, getattr(RasterLayer, 'enddate')>= value).filter(RasterLayer.dataset_id == Dataset.id)
            value = strptime(filters['enddate'], "%Y-%m-%d")
            query=query.outerjoin(RasterLayer).filter(getattr(RasterLayer, 'startdate') <= value, getattr(RasterLayer, 'enddate')>= value).filter(RasterLayer.dataset_id == Dataset.id)
            print(value)
            print('QUERYYYYYYYYYYYYYYYYYY')
            del filters['startdate']
            del filters['enddate']
        
        #add filters
        for attr, value in filters.items():
            if hasattr(Dataset, attr):
                query = query.filter(getattr(Dataset, attr) == value)
            elif hasattr(RasterLayer, attr): #join tables
                print('JOIN TABLES')
                #query.filter(RasterLayer.dataset_id.any(RasterLayer.dataset_id == 'dem'))
                #pass            
                #query2=self.Session.query(RasterLayer.dataset_id)
                '''try:
                    rasterlayer= query2.filter(getattr(RasterLayer, attr) == value)
                except:
                    rasterlayer = []
                print(rasterlayer.all())
                print(rasterlayer)'''
                query=query.outerjoin(RasterLayer).filter(getattr(RasterLayer, attr) == value).filter(RasterLayer.dataset_id == Dataset.id)
                #query.filter(Dataset.id.in_(rasterlayer))

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
            except:
                return []
        else: 
            try:
                result=query.all() 
                if orderbyarea:
                    result.sort(key=lambda x: x.area, reverse=True)
                return self.asDictionary(result, timelayers=timelayers) 
            except Exception as e:
                print('Exception ',e)
                print('No results found')
                geoCollection = {}
                geoCollection['type']= 'FeatureCollection'
                geoCollection['features'] = []
                return geoCollection
    

    
    
    def getRasterLayers(self, filters={}):
        """returns a list of all requested datasets.
        
        Input parameter:
            filters – (optional) a list of filteroptions
                e.g. filters={'dataset_id' : 1, 'layertype' : 'dem'}
            dic – true if result should be returned as dictionnary
                
        Returns:
            a list with Dataset objects/ one object or a dictionnary
        
        """

        query = self.Session.query(RasterLayer)
        
        for attr, value in filters.items():
            query = query.filter(getattr(RasterLayer, attr) == value)
        
        #query=query.filter(filterrule)
        try:
            return query.all()
        except Exception as e:
            #print (e)
            return []
    
    
    def getLayers(self, filters={}):
        """returns a list of all requested layers.
        
        Input parameter:
            filters – (optional) a list of filteroptions
                e.g. filters={'dataset_id' : 1, 'layertype' : 'dem'}
            dic – true if result should be returned as dictionnary
                
        Returns:
            a list with Dataset objects/ one object or a dictionnary
        
        """

        result = self.getRasterLayers(filters=filters)
        result.sort(key=lambda x: x.layertype, reverse=False)
        ## if pointlayer in database they would be added here to the result
        return result
    
    
    
    
    def asDictionary(self, datasets, timelayers=False):
        '''Returns a list of datasets as dictionary in GeoJSON format'''
        features=[]
        for ds in datasets:
            geodic = ds.asGeoDict()
            layers = self.getLayers({'dataset_id' : ds.id})
            layers_dict=[]
            for l in layers:
                l_dict=l.asDict()
                #tile_url = self.conf.getRelativeTilesFolder(l)
                #l_dict['tileurl'] = tile_url
                if timelayers:
                    print('yeah')
                    l_dict['timeseries'] = self.getTimeSeriesDict(l)
                #l_dict['layertype']=self.getLayertypeById(l.layertype).name
                layers_dict.append(l_dict)
                
            geodic['properties']['layers'] = layers_dict
            features.append(geodic)
            
        #print(geoDict)
        geoCollection = {}
        geoCollection['type']= 'FeatureCollection'
        geoCollection['features'] = features
    
        return geoCollection
    
   
    def getTimeSeriesDict(self, layer):
        timeseries = []
        dates = self.conf.getTimeseries(layer)
        for val in reversed(dates):
            tile = self.conf.getRelativeTilesFolder(layer, val)
            timeseries.append({'date': val, 'tileurl': tile})
        return timeseries
    
    
    
    def updateTimestamp(self, layer, commit=True):
        
        assert self.Session is not None
        
        time = datetime.utcnow() 
        
        layer.timestamp = time
        if commit:
            self.Session.commit()
        else:
            self.Session.flush()
            
            
    def updateTimeSeries(self, layer, startdate=None, enddate=None, commit=True):
        '''Updates a layers start if the new time layer is not within the old time span'''
        assert self.Session is not None
        if enddate is not None:
            layer.enddate = enddate
        if startdate is not None:
            layer.startdate = startdate
        if commit:
            self.Session.commit()
        else:
            self.Session.flush()
        


    
    
    
    """def getRasterLayers(self, dic=None):
        query = self.Session.query(RasterLayer)
        
           
        result=query.all()
        
        if not dic:
            return result
        else: 
            return self.asDictionary(result) """
    
    
    
    
    
    '''def getLayertypeByName(self, tname):
        query = self.Session.query(LayerType)
        query=query.filter(LayerType.name == tname)
        try:
            return query.first()
        except Exception as e:
            print (e)
            return [] '''
        
    '''def getLayertypeById(self, tid):
        query = self.Session.query(LayerType)
        query=query.filter(LayerType.id == tid)
        try:
            return query.first()
        except Exception as e:
            print (e)
            return [] '''
           
    
    '''def getLayerById(self, l_id):

        query = self.Session.query(RasterLayer)
        query=query.filter(RasterLayer.id == l_id)
        try:
            return query.all()
        except Exception as e:
            print (e)
            return []'''    
    
    
    
    '''def getLayersByDataset(self, dataset_id):
        """returns a list of all requested datasets.
        
        Input parameter:
            ids – (optional) a list of integers or one single integer
                when ids is given only the requested datasets with matching ids are returned
                when ids is none every dataset is returned
        
        Returns:
            a list with Dataset objects/ one object
        
        """
        query = self.Session.query(RasterLayer)
        print('datasetid ',dataset_id)
        query=query.filter(RasterLayer.dataset_id == dataset_id)
        try:
            return query.all()
        except Exception as e:
            print (e)
            return [] ##empty array'''
    
        
    
    
    '''def getLayerTypes(self, ids=None, dic=False):
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
        result = query.all()
        if not dic:      
            return result
        else: #return a dictionary
            types=[]
            for l in result:
                types.append(l.asDict())
            dic={}
            dic['layertypes']=types
            return dic'''
    
    '''def getProjections(self, ids=None):
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
            
        return query.all()'''
    


        
    '''def newLayerType(self, name, commit=True):
        
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
            raise'''
        
        
        
    '''def newProjection(self, name, commit=True):
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
            raise'''