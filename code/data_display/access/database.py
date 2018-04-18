#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:27:30 2018

@author: livia
"""

#import cx_Oracle
#from .file import Class1, Class2

import sqlite3


__all__ = ['Database']

class Database(object):
    """This object controls all interactions with the database
    This class contains all functionality to:
    1) Open and close the connection
    2) Load metadata
    """
    
    def __init__(self, dbdir="../../metadata.db"):
        """Initialise and set connection to None"""
        self._conn = None
        self._dbdir = dbdir
    
    def openConnection(self):
        """Open Connection"""
        #pwdPath = "../../../oracle/mainpwd"
        #userPath = "../../../oracle/username"
        #with open(pwdPath,'r') as pwdRaw:
        #	pwd = pwdRaw.read().strip()
        #with open(userPath,'r') as userRaw:
        #	username = userRaw.read().strip()
        #self._conn = cx_Oracle.connect(dsn="geosgen",user=username,password=pwd)
        #pwd = None #Keep Pwd in memory for a short as possible
        self._conn = sqlite3.connect(self._dbdir)
        pass
        
    
    def closeConnection(self):
        """Close Connection"""
        
        assert self._conn != None #Check connection open
        self._conn.close
        self._conn = None

    
    def addDataSet(self):
        """Adds a new dataset"""
        
        pass

