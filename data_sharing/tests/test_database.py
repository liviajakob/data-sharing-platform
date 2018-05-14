'''
@author: livia
'''
import unittest
from display_data import Database
import sys, os




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
        self.assertEqual(len(self.db.getTableNames()), 4, "Database should have 4 tables")
        
    def test_noEntries(self):
        self.assertEqual(len(self.db.getDatasets()), 0, "No table entries for projections should exist")
        self.assertEqual(len(self.db.getProjections()), 0, "No table entries for projections should exist")
    
    
    def test_dbInsert(self):
        '''Test insert values into database'''
        #insert 2 projections
        self.db.newLayerType("dem")
        self.db.newLayerType("error")
        self.db.newLayerType("rate")
        self.db.newProjection("Projection1")
        self.db.newProjection("Projection2")
        self.db.newDataset("this is how", 1)
        self.db.newDataset("cite...", 1)
        self.db.newDataset("this is how you cite", 2)
        self.db.newLayer(1, "dem")
        self.db.newLayer(1, "error")
        
        self.db.commit()
        
        self.assertEqual(len(self.db.getDatasets()), 3, "couldnt insert all datasets")
        self.assertEquals(len(self.db.getProjections()), 2, "couldnt insert all projections")
        self.assertEquals(self.db.getDatasets(2)[0].id, 2, "Error in get Datasets")
        self.assertEquals(len(self.db.getDatasets([2,3])), 2, "Error in get Datasets")
        self.assertEquals(len(self.db.getLayerTypes()), 3, "couldnt insert all layer types")
        self.assertEquals(len(self.db.getLayerByAttributes()), 2, "couldnt insert all layers")
        
        print("TYPE: ----------------------------------------", self.db.getLayerByAttributes()[0].timestamp)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    print("FIIIIIIILE",__file__)