'''
Created on 25 Apr 2018

@author: livia
'''

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
#from sqlalchemy import desc, func
#import datetime

Base = declarative_base()



"""class Projection(Base):
    '''Represents a Projection table'''
    __tablename__ = 'projection'
    id=Column('id',Integer, primary_key=True)
    name = Column(String(250), unique=True)

    
    def __str__(self):
        return "PROJECTION: id={} name={}".format(self.id, self.name)"""
    


class Dataset(Base):
    '''Represents a dataset table'''
    __tablename__ = 'dataset'
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
    #ForeignKey("projection.id")
    #projection = relationship("Projection", backref=backref("dataset"))
    
    def getBoundingBox(self):
        return {'xmin':self.xmin,'xmax': self.xmax, 'ymin':self.ymin,'ymax': self.ymax}
    
    
    def asGeoDict(self):
        '''Returns a dict which can be used to convert to a geoJSON'''
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
        return "DATASET: id={} cite={}".format(self.id, self.cite)
   
   
   
class RasterLayer(Base):
    '''Represents a layerType table'''
    __tablename__ = 'rasterlayer'
    id = Column('id',Integer, primary_key=True)
    #timestamp = Column(DateTime(timezone=True), server_default=func.now())
    dataset_id =Column(Integer(), ForeignKey("dataset.id"))
    dataset = relationship("Dataset", backref=backref("layer"))
    layertype = Column(String()) # '''ForeignKey("layerType.id")'''
    startdate = Column(DateTime(timezone=True))
    enddate = Column(DateTime(timezone=True))
    #layerType = relationship("LayerType", backref=backref("layer"))
    
    def asDict(self):
        '''Returns a dict which can be used to convert to a JSON'''
        dic = {}
        dic['id']=self.id
        #dic['timestamp']=self.timestamp
        dic['layertype']=self.layertype
        dic['startdate']=str(self.startdate.strftime("%Y-%m-%d"))
        dic['enddate']=str(self.enddate.strftime("%Y-%m-%d"))
        
        return dic
    
    def __str__(self):
        return "LAYER: id={} datasetid={}".format(self.id, self.dataset_id)
       
   
"""class LayerType(Base):
    '''Represents a layertype table'''
    __tablename__ = 'layerType'
    id = Column('id',Integer, primary_key=True)
    name = Column(String(250), unique=True)
    
    
    def __str__(self):
        return "LAYERTYPE: id={} name={}".format(self.id, self.name)
 
    def asDict(self):
        '''Returns a dict which can be used to convert to a JSON'''
        dic = {}
        dic['id']=self.id
        dic['name']=self.name
        return dic
    """
 
    
def createModels(engine):
    '''Creates all tables'''
    Base.metadata.create_all(bind=engine)
    