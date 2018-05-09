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
        self.outputfile = os.path.join(dir_path, "testdata","test_proc_output.tif")
        self.outputfile_colour = os.path.join(dir_path, "testdata","test_proc_output_col.tif")
        self.colourfile = os.path.join(dir_path, "testdata","colours.txt")
        #remove if already exists
        #try:
        #    os.remove(self.outputfile)
        #except OSError:
        #    pass
        
        ## database
        #dbpath= os.path.join(dir_path, "testdata")
        #dbdict={"name":"test.db",
        #      "path":dbpath,
        #      "type": "sqlite:///"
        #      }
        #self.db = Database(dbSettings=dbdict)
        #self.db.scopedSession()

        
    def tearDown(self):
        pass


    def test_readRaster(self):
        raster_proc = RasterLayerProcessor(layertype="dem", logger=self.logger)
        raster_proc.readFile(self.inputfile)
        box = raster_proc.getBoundingBox()
        result = {'upleft': (-1771834.5, -521176.688), 'downright': (2117165.5, -3433176.688)}
        self.assertEqual(box, result)
        raster_proc.getStatistics()
        
        
        
    def test_getProjection(self):
        '''Tests the method getProjection'''
        raster_proc = RasterLayerProcessor(layertype="dem", logger=self.logger)
        raster_proc.readFile(self.inputfile)
        proj = raster_proc.getProjection()
        self.assertEqual(proj.GetAttrValue('PROJECTION'), 'Polar_Stereographic')




    def test_conversion(self):
        '''Tests the conversion of a raster using the gdal commandline tool'''
        raster_proc = RasterLayerProcessor(layertype="dem", logger=self.logger)
        raster_proc.to8Bit(inputfile=self.inputfile, outputfile=self.outputfile, scale={'min': 0, 'max': 3277},)
        self.assertTrue(os.path.exists(self.outputfile))
        raster_proc.readFile(self.outputfile)
        print(raster_proc.getColourTable())
        #self.assertIsNone(raster_proc.getColourTable())
        raster_proc.addColours(inputfile=self.outputfile, outputfile=self.outputfile_colour, colourfile=self.colourfile) # take the above computed as input
        print(raster_proc.getColourTable())
        self.assertTrue(os.path.exists(self.outputfile_colour))
        




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()