'''
Created on 9 May 2018

@author: livia
'''
import unittest
import sys
import logging
import os
from display_data import RasterLayerProcessor


class Test(unittest.TestCase):


    def setUp(self):
        
        logging.basicConfig(level=logging.INFO) #NOTSET gives all the levels, e.g. INFO only .info
        self.logger = logging.getLogger(__name__)
        
        module_path = sys.modules[__name__].__file__
        dir_path = os.path.dirname(module_path)
        self.inputfile = os.path.join(dir_path,"testdata","test_proc.tif")
        self.inputfile_cropped = os.path.join(dir_path,"testdata","test_cut.tif")
        
        

    def tearDown(self):
        pass


    def test_minBoundingBox(self):
        raster_proc = RasterLayerProcessor(layertype="dem", logger=self.logger)
        raster_proc.readFile(self.inputfile)
        self.assertNotEqual(raster_proc.getMinBoundingBox(),raster_proc.getBoundingBox())
        print('BOUNDING 1', raster_proc.getBoundingBox())


    def test_minBoundingBoxWithCropped(self):
        raster_proc = RasterLayerProcessor(layertype="dem", logger=self.logger)
        raster_proc.readFile(self.inputfile_cropped)
        self.assertEqual(raster_proc.getMinBoundingBox(),raster_proc.getBoundingBox())



    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_minBoundingBox']
    unittest.main()