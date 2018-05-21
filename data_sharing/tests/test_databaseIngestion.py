'''
@author: livia
'''
import unittest
from display_data import Database, Rollback, DatabaseIngestion
import sys, os
import logging




class DatabaseIngestionTest(unittest.TestCase):
    '''This test class tests all functionality of the Database and Modules'''

    def setUp(self):
        '''Sets up a test database'''
        module_path = sys.modules[__name__].__file__
        dir_path = os.path.dirname(module_path)
        path= os.path.join(dir_path, "testdata")
        dbdict={"name":"test.db",
              "path":path,
              "type": "sqlite:///"
              }
        self.db = Database(dbSettings=dbdict)
        self.db.scopedSession()
        self.db.dropTables('livia')
        self.db.createTables()
        
        self.db.newLayerType("dem")
        self.db.newLayerType("error")
        self.db.newLayerType("rate")
        self.db.newProjection("Projection1")
        self.db.newProjection("Projection2")
        self.db.closeSession()
        
        logging.basicConfig(level=logging.INFO) #NOTSET gives all the levels, e.g. INFO only .info
        self.logger = logging.getLogger(__name__)
        
        rollback=Rollback(self.logger)
        
        self.insert=DatabaseIngestion(rollback=rollback, logger=self.logger, database=self.db)
        #self.insert.addDataset(layers=None, cite='hi')

        


    def tearDown(self):
        '''Drops the tables and closes the connection'''
        self.db.dropTables("livia")
        self.db.closeSession()


    def test_dbInsert(self):
        '''Test insert values into database'''
        #self.insert.addDataset(layers=None, cite='hi')
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    print("FIIIIIIILE",__file__)