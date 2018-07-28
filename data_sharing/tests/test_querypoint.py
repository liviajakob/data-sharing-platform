'''
Unittests for query_point.py module in get_data package
File: test_querypoint.py

@author: livia
'''
import unittest, sys, os
from get_data.query_point import retrieve_pixel_value
import numpy as np


class QueryPointTest(unittest.TestCase):


    def testRetrievePixelValue(self):
        '''Tests the retrieve_pixel_value() function'''
        module_path = sys.modules[__name__].__file__
        dir_path = os.path.dirname(module_path)
        path= os.path.join(dir_path, "testdata")
        fname= os.path.join(path, "test_cut.tif")
        coords=[-102834.5, -2151176.688]
        value = retrieve_pixel_value(coords, fname)
        self.assertEqual(value, 115.0)
        
    def testCoordinatesOutOfBound(self):
        '''Tests behaviour when coordinates are out of file boundaries'''
        module_path = sys.modules[__name__].__file__
        dir_path = os.path.dirname(module_path)
        path= os.path.join(dir_path, "testdata")
        fname= os.path.join(path, "test_cut.tif")
        coords=[34,235]
        value = retrieve_pixel_value(coords, fname)
        self.assertTrue(np.isnan(value))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()