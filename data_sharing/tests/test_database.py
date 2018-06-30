'''
@author: livia
'''
import unittest
from display_data import Database
import sys, os
from numpy.lib.tests.test_io import strptime
from datetime import datetime




class DatabaseTest(unittest.TestCase):
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
        


    def tearDown(self):
        '''Drops the tables and closes the connection'''
        self.db.dropTables("livia")
        self.db.closeSession()


    def test_tablesCreated(self):
        '''Check if it has created the tables'''
        self.assertEqual(len(self.db.getTableNames()), 2, "Database should have 2 tables")
        
    def test_noEntries(self):
        self.assertEqual(len(self.db.getDatasets()), 0, "No table entries for projections should exist")
        self.assertEqual(len(self.db.getRasterLayers()), 0, "No table entries for layers should exist")
    
    
    def test_dbInsert(self):
        '''Test insert values into database'''
        self.db.newDataset("this is how", 'EPSG:3413')
        self.db.newDataset("cite...", 'EPSG:3413')
        self.db.newDataset("this is how you cite", 'EPSG:3413')
        self.db.newRasterLayer(1, "dem", strptime('2017-06-26', "%Y-%m-%d"))
        self.db.newRasterLayer(1, "error", strptime('2017-06-29', "%Y-%m-%d"))
        self.db.newRasterLayer(2, "dem", strptime('2017-06-26', "%Y-%m-%d"))
        
        self.db.commit()
        
        self.assertEqual(len(self.db.getDatasets()), 3, "couldnt insert all datasets")
        self.assertEquals(self.db.getDatasets(filters={'id' : 2})[0].id, 2, "Error in get Datasets")
        self.assertEquals(len(self.db.getDatasets()), 3, "Error in get Datasets")
        self.assertEquals(len(self.db.getDatasets(filters={'layertype':'dem'})), 2, "Error in get Datasets")
        self.assertEquals(len(self.db.getDatasets(filters={'layertype':'error'})), 1, "Error in get Datasets")
        filters={'dataset_id' : 1, 'layertype' : 'dem'}
        self.assertEquals(self.db.getRasterLayers(filters)[0].layertype, 'dem', "couldnt insert dem layer")
        self.assertEquals(self.db.getRasterLayers(filters)[0].enddate, datetime(2017, 6, 26, 0, 0), "couldnt insert dem layer")
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()