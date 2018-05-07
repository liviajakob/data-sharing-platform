'''
Created on 6 May 2018

@author: livia
'''
import unittest
from display_data import Tiler
import sys
import os
import shutil


class TilerTest(unittest.TestCase):


    def setUp(self):
        module_path = sys.modules[__name__].__file__
        dir_path = os.path.dirname(module_path)
        self.inputfile = os.path.join(dir_path,"testdata","test.tif")
        self.outputdir = os.path.join(dir_path, "testdata","output")
        # remove output folder if exists
        if os.path.exists(self.outputdir):
            shutil.rmtree(self.outputdir) 
            
        self.tiler = Tiler()
        self.tiler.createTiles(self.inputfile, self.outputdir)



    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()