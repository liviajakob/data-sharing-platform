'''
@author: livia
'''
import unittest
from display_data import Database


class DatabaseTest(unittest.TestCase):
    '''This test class tests all functionality of the Database and Modules'''

    def setUp(self):
        '''Sets up a test database'''
        self.db = Database("test.db")
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
        self.assertEqual(len(self.db.getProjections()), 0, "No table entries for projections should exist")
    
    
    def test_dbInsert(self):
        '''Test insert values into database'''
        #insert 2 projections
        self.db.newProjection("Projection1")
        self.db.newProjection("Projection2")
        self.db.newDataset("Dataset1", "this is how", 1)
        self.db.newDataset("Dataset2", "cite...", 1)
        self.db.newDataset("Dataset3", "this is how you cite", 2)
        
        self.assertEqual(len(self.db.getDatasets()), 3, "couldnt insert all datasets")
        self.assertEquals(len(self.db.getProjections()), 2, "couldnt insert all projections")
        self.assertEquals(self.db.getDatasets(2)[0].name, "Dataset2", "Error in get Datasets")
        self.assertEquals(len(self.db.getDatasets([2,3])), 2, "Error in get Datasets")
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()