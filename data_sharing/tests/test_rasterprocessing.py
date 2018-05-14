'''
Created on 8 May 2018

@author: livia
'''
import unittest
import sys
import logging
import os
from display_data import RasterLayerProcessor


class DEMRAsterProcessing(unittest.TestCase):
    
    def setUp(self):
        
        logging.basicConfig(level=logging.INFO) #NOTSET gives all the levels, e.g. INFO only .info
        self.logger = logging.getLogger(__name__)
        
        module_path = sys.modules[__name__].__file__
        dir_path = os.path.dirname(module_path)
        self.inputfile = os.path.join(dir_path,"testdata","test_proc.tif")
        self.outputfile_conv = os.path.join(dir_path, "testdata","test_proc_output_conv.tif")
        self.outputfile_cut = os.path.join(dir_path, "testdata","test_proc_output_cut.tif")
        self.outputfile_colour = os.path.join(dir_path, "testdata","test_proc_output_col.tif")
        self.colourfile = os.path.join(dir_path, "testdata","colours.txt")
        #remove if already exists
        #try:
        #    os.remove(self.outputfile_conv)
        #except OSError:
        #    pass


        
    def tearDown(self):
        pass


    def test_readRaster(self):
        '''Tests the method read Raster'''
        raster_proc = RasterLayerProcessor(logger=self.logger)
        raster_proc.readFile(self.inputfile)
        box = raster_proc.getBoundingBoxCorners()
        result = {'upleft': (-1771834.5, -521176.688), 'downright': (2117165.5, -3433176.688)}
        self.assertEqual(box, result)
        stats = {'min': 0.0, 'max': 3277.0476074219, 'mean': 2178.9048430742, 'stdev': 680.47755318626}
        self.assertEqual(raster_proc.getStatistics(), stats)
        
        
        
    def test_getProjection(self):
        '''Tests the method getProjection'''
        raster_proc = RasterLayerProcessor(logger=self.logger)
        raster_proc.readFile(self.inputfile)
        proj = raster_proc.getProjection()
        self.assertEqual(proj.GetAttrValue('PROJECTION'), 'Polar_Stereographic')




    def test_conversion(self):
        '''Tests the conversion of a raster using the gdal commandline tool'''
        raster_proc = RasterLayerProcessor(logger=self.logger)
        
        #convert to 8bit
        raster_proc.to8Bit(inputfile=self.inputfile, outputfile=self.outputfile_conv, scale={'min': 0.0, 'max': 3277.0476074219},)
        self.assertTrue(os.path.exists(self.outputfile_conv))
        raster_proc.readFile(self.outputfile_conv)
        minbound = raster_proc.getMinBoundingBox()
        
        #cut raster
        raster_proc.cutRaster(inputfile=self.outputfile_conv, outputfile=self.outputfile_cut)
        self.assertTrue(os.path.exists(self.outputfile_cut))
        raster_proc.readFile(self.outputfile_cut)
        bound =  raster_proc.getBoundingBox()
        #check if raster is cut to min size
        self.assertEqual(bound, minbound, 'Raster not properly cut')
        
        #add colour
        raster_proc.addColours(inputfile=self.outputfile_cut, outputfile=self.outputfile_colour, colourfile=self.colourfile) # take the above computed as input
        self.assertTrue(os.path.exists(self.outputfile_colour))
        




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()