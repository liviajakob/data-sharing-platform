'''
Unittests for the RasterLayerProcessor
File: prepare_raster.py

@author: livia
'''
import unittest
import sys
import logging
import os
from display_data import RasterLayerProcessor


class DEMRAsterProcessing(unittest.TestCase):
    
    def setUp(self):
        '''Set up environment'''
        logging.basicConfig(level=logging.INFO) #NOTSET gives all the levels, e.g. INFO only .info
        self.logger = logging.getLogger(__name__)
        module_path = sys.modules[__name__].__file__
        dir_path = os.path.dirname(module_path)
        self.inputfile = os.path.join(dir_path,"testdata","test_proc.tif")
        self.outputfile_cut = os.path.join(dir_path, "testdata","test_proc_output_cut.tif")
        self.outputfile_colour = os.path.join(dir_path, "testdata","test_proc_output_col.tif")
        self.colourfile = os.path.join(dir_path, "testdata","colours.txt")


    def test_readRaster(self):
        '''Tests the method readRaster'''
        raster_proc = RasterLayerProcessor(logger=self.logger)
        raster_proc.readFile(self.inputfile)
        box = raster_proc.getBoundingBoxCorners()
        print(box)
        result = {'upleft': (-50.48764491820475, 67.32946338522015), 'downright': (-49.405871523253154, 66.7586531752604)}
        self.assertEqual(box, result)
        
        

    def test_conversion(self):
        '''Tests the conversion of a raster using the gdal commandline tool'''
        raster_proc = RasterLayerProcessor(logger=self.logger)
        raster_proc.readFile(self.inputfile)
        minbound = raster_proc.getMinBoundingBox()
        
        #cut raster
        raster_proc.cutRaster(inputfile=self.inputfile, outputfile=self.outputfile_cut)
        self.assertTrue(os.path.exists(self.outputfile_cut))
        raster_proc.readFile(self.outputfile_cut)
        bound =  raster_proc.getExtent()
        #check if raster is cut to min size
        self.assertEqual(bound, minbound, 'Raster not properly cut')
        
        #add colour
        raster_proc.addColours(inputfile=self.outputfile_cut, outputfile=self.outputfile_colour, colourfile=self.colourfile) # take the above computed as input
        self.assertTrue(os.path.exists(self.outputfile_colour))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()