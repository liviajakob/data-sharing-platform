'''
Unittests for minimum bounding box calculation in prepare_raster.py
File: test_minBoundingBox.py

@author: livia
'''
import unittest
import sys, logging, os
from display_data import RasterLayerProcessor


class MinBoundingBoxTest(unittest.TestCase):

    def setUp(self):
        '''Set up environment'''
        logging.basicConfig(level=logging.INFO) #NOTSET gives all the levels, e.g. INFO only .info
        self.logger = logging.getLogger(__name__)
        
        module_path = sys.modules[__name__].__file__
        dir_path = os.path.dirname(module_path)
        self.inputfile = os.path.join(dir_path,"testdata","test_proc.tif")
        self.inputfile_cropped = os.path.join(dir_path,"testdata","test_cut.tif")
            

    def test_minBoundingBox(self):
        '''Test minBoundingBox is equal to extent'''
        raster_proc = RasterLayerProcessor(logger=self.logger)
        raster_proc.readFile(self.inputfile)
        self.assertNotEqual(raster_proc.getMinBoundingBox(),raster_proc.getExtent())


    def test_minBoundingBoxWithCropped(self):
        '''Test minBoundingBox with cropped file is equal to extent'''
        raster_proc = RasterLayerProcessor(logger=self.logger)
        raster_proc.readFile(self.inputfile_cropped)
        self.assertEqual(raster_proc.getMinBoundingBox(),raster_proc.getExtent())



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_minBoundingBox']
    unittest.main()