'''
Created on 25 Apr 2018

@author: livia
'''

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
#from sqlalchemy import desc, func

Base = declarative_base()



class Projection(Base):
    '''Represents a Projection table'''
    __tablename__ = 'projection'
    id=Column('id',Integer, primary_key=True)
    name = Column(String(250), unique=True)

    
    def __str__(self):
        return "PROJECTION: id={} name={}".format(self.id, self.name)
    


class Dataset(Base):
    '''Represents a dataset table'''
    __tablename__ = 'dataset'
    id = Column('id',Integer, primary_key=True)
    name = Column(String(250), unique=True)
    cite = Column(String(250), nullable=False)
    projection_id=Column(Integer(), ForeignKey("projection.id"))
    projection = relationship("Projection", backref=backref("dataset"))
    
    
    def __str__(self):
        return "DATASET: id={} name={} cite={}".format(self.id, self.name, self.cite)
    
 
    
def createModels(engine):
    '''Creates all tables'''
    Base.metadata.create_all(bind=engine)
    

