'''
Contains all the database models to create and map database tables
File: models.py

@author: livia
'''

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import UniqueConstraint

#Use of the decalrative extension of SQLAlchemy
Base = declarative_base()



class Dataset(Base):
    '''Class to represent a dataset database table
    An instance of the class represents one row of the table
    
    Inherits from Base from the declarative API
    '''
    __tablename__ = 'dataset'
    
    #table columns
    id = Column('id',Integer, primary_key=True)
    cite = Column(String(250), nullable=False)
    xmin = Column(Float)
    xmax = Column(Float)
    ymin = Column(Float)
    ymax = Column(Float)
    area = Column(Float)
    startdate = Column(DateTime(timezone=True))
    enddate = Column(DateTime(timezone=True))
    projection=Column(String()) # this is the projection the dataset xmin, xmax etc. are in
    
    def getExtent(self):
        '''Returns the extent of the dataset
        
        Returns:
            a dictionnary containing the keys:
                'xmin' - min x value
                'xmax' - max x value
                'ymin' - min y value
                'ymax' - max y value
        '''
        return {'xmin':self.xmin,'xmax': self.xmax, 'ymin':self.ymin,'ymax': self.ymax}
    
    
    def asGeoDict(self):
        ''' Returns a dictionary which can be used to convert to a GeoJSON 
        Dataset extents are represented by GeoJSON polygon geometries
        
        '''
        dic = {}
        dic['type']="Feature"
        dic['properties']={}
        dic['properties']['id']=self.id
        dic['properties']['cite']=self.cite
        dic['properties']['area']= self.area/1000000 # in km2
        dic['properties']['startdate']=str(self.startdate.strftime("%Y-%m-%d"))
        dic['properties']['enddate']=str(self.enddate.strftime("%Y-%m-%d"))
        dic['properties']['projection']=self.projection
        dic['geometry']={}
        dic['geometry']['type']="Polygon"
        dic['geometry']['coordinates']=[[[self.xmin,self.ymin],[self.xmax,self.ymin], [self.xmax,self.ymax], [self.xmin,self.ymax], [self.xmin,self.ymin]]]
        return dic

    
    
    def __str__(self):
        return "Dataset: id={}".format(self.id)
   
   
   
class RasterLayerGroup(Base):
    '''Class to represent a rasterlayer group database table
    An instance of the class represents one row of the table
    
    Inherits from Base from the declarative API
    '''
    __tablename__ = 'rasterlayergroup'
    
    # table columns
    id = Column('id',Integer, primary_key=True)
    dataset_id =Column(Integer(), ForeignKey("dataset.id"))
    dataset = relationship("Dataset", backref=backref("layer"))
    layertype = Column(String()) #unique
    startdate = Column(DateTime(timezone=True))
    enddate = Column(DateTime(timezone=True))
    UniqueConstraint('dataset_id', 'layertype', name='uix_1')
    
    def asDict(self):
        '''Returns itself represented as a dictionary 
        which can be used to convert to a JSON
        
        '''
        dic = {}
        dic['id']=self.id
        dic['layertype']=self.layertype
        dic['startdate']=str(self.startdate.strftime("%Y-%m-%d"))
        dic['enddate']=str(self.enddate.strftime("%Y-%m-%d"))
        return dic
    
    
    def __str__(self):
        return "Rasterlayer: id={} type={} datasetid={}".format(self.id, self.layertype, self.dataset_id)
       
 
    
def createModels(engine):
    '''Creates all database tables from the models
    
    Input Parameter:
        engine - database engine
    '''
    Base.metadata.create_all(bind=engine)
    