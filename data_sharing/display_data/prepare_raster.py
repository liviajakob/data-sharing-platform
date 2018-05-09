'''Contains all the classes to process a raster and prepare it for webdisplay

@author: livia

'''

import subprocess
import gdal
import osr
import numpy as np

class RasterTiler(object):
    '''
    Creates tiles
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    
    def createTiles(self, inputfile, outputdir, colours = None, zoom="0-5"):
        commandlist=['gdal2tiles.py', '-z', zoom, '-p', 'raster', inputfile, outputdir]
        print(commandlist)
        subprocess.call(commandlist)
    
    
    
    
    
    
###################################################    
    
class RasterLayerProcessor(object):
    '''
    Creates Layer entries
    '''
    
    
    
    def __init__(self, layertype, logger):
        '''
        Constructor
        '''
        self.logger = logger
        self.raster = None
        self.band = None
        self.raster_8bit = None
        self.type = layertype
        
        
    
    def layerExists(self):
        return False
    
    
    def layerUpdated(self):
        pass
   
   
    def readFile(self, inputfile, band=1):
        '''read raster file with gdal'''
        self.logger.info("Starting to read raster...")
        self.raster = gdal.Open(inputfile)
        self.logger.info("Read raster...")
        self.band = self.raster.GetRasterBand(band) #for now I assume there is only one band

    def getStatistics(self):
        stats = self.band.GetStatistics(True, True)
        statsdir = {'min' : stats[0], 'max': stats[1], 'mean' : stats[2], 'stdev' : stats[3]}
        #print(statsdir)
        #print ("[ NO DATA VALUE ] = ", self.band.GetNoDataValue()) # none
        #print ("[ SCALE ] = ", self.band.GetScale())
        #print ("[ UNIT TYPE ] = ", self.band.GetUnitType())
        return statsdir

    def getProjection(self):
        '''Generates a wkt and converts it to SpatialReference object
        
        Returns:
            a SpatialReference object
        
        '''
        prj = self.raster.GetProjection()
        srs=osr.SpatialReference(wkt=prj)
        #if srs.IsProjected:
            #print ('proj',srs.GetAttrValue('projcs'))        
        return srs

    
    def getBoundingBox(self):
        '''Returns the bounding box of the raster (upper left corner and lower right corner)
        
        Returns:
            A dictionary - {"upleft": (ulx, uly), "downright": (lrx, lry)}
        
        '''
        assert self.raster is not None
        ulx, xres, xskew, uly, yskew, yres  = self.raster.GetGeoTransform()
        lrx = ulx + (self.raster.RasterXSize * xres)
        lry = uly + (self.raster.RasterYSize * yres)
        #ulx, uly: upper left corner
        #lrx, lry: lower right corner
        return {'upleft': (ulx, uly), 'downright': (lrx, lry)}
    
    
    
    # @TODO check if min > max
    def getMinBoundingBox(self):
        '''Calculates a min boundingbox without cutting not Null values
        
        Returns:
            {xmin: coord, xmax: coord, ymin: coord, ymax: coord}
        
        '''
        grid = self.raster.ReadAsArray()
        print(grid)
        print(self.band.GetNoDataValue())
        # create 1D array (x-direction) with True values where the whole column/raster of the raster is Null
        if self.band.GetNoDataValue() is None:
            xArr = np.all(np.isnan(grid), axis = 0)
            yArr = np.all(np.isnan(grid), axis = 1)
        else:
            xArr = np.all(grid==self.band.GetNoDataValue(), axis = 0)
            yArr = np.all(grid==self.band.GetNoDataValue(), axis = 1)    
        
        
        print(xArr.shape)
        xContent = np.where(np.invert(xArr))
        minX, maxX = xContent[0][0]-1, xContent[0][-1]+1

        
        print(yArr.shape)
        print(yArr)
        # calculate indices where yArr is False
        yContent = np.where(np.invert(yArr))
        print(yContent)
        minY, maxY = yContent[0][0]-1, yContent[0][-1]+1
        
        ## adjust if out of boundary
        if minX < 0: minX = 0
        if maxX > len(xArr): maxX = len(xArr)
        if minY < 0: minY = 0
        if maxY > len(yArr): maxY = len(yArr)
        
        #calculate coordinates
        ulx, xres, xskew, uly, yskew, yres  = self.raster.GetGeoTransform() # get corrdinates and resolution
        minXc = ulx + (minX * xres)
        maxXc = ulx + (maxX * xres)
        minYc = uly + (minY * yres)
        maxYc = uly + (maxY * yres)
        
        #Flip if min and max are exchanged
        if minXc > maxXc: minXc, maxXc = maxXc, minXc
        if minYc > maxYc: minYc, maxYc = maxYc, minYc
        
        return {'xmin': minXc, 'xmax': maxXc, 'ymin': minYc, 'ymax': maxYc}

    
    # @Todo several checks
    def cutRaster(self, inputfile, outputfile, boundbox={}):
        '''Cuts the raster to a desired ...
        
        Default cuts the minimum boundingbox for not NaN values
        
        '''
        # check if bounding box input is given
        if not boundbox:
            boundbox = self.getMinBoundingBox() # calculate bounding box 
        
        commandlist=['gdalwarp', '-te', str(boundbox['xmin']), str(boundbox['ymin']), str(boundbox['xmax']), str(boundbox['ymax']), '-overwrite', inputfile, outputfile]
        print(commandlist)
        subprocess.call(commandlist)
        
    
    
    # @TODO not hardcoded!
    def to8Bit(self, inputfile, outputfile, scale, fileformat='GTiff', exponent=2, bits=[1,255], nodata=0):
        '''Converts the raster to 8-bits
        
        Input Params:
            scale -- [minraster, maxraster, min_newraster, max_newraster]
        
        '''
        
        self.logger.info('Converting raster to 8 Bit...')
        commandlist=['gdal_translate', '-ot', 'Byte', '-of', fileformat, '-scale', str(scale['min']), str(scale['max']), str(bits[0]), str(bits[1]),'-exponent', str(exponent), '-a_nodata', str(nodata), inputfile, outputfile]
        subprocess.call(commandlist)

        self.logger.info('Finished converting to 8 Bit')
        
    
    
    def addColours(self, inputfile, outputfile, colourfile):
        self.logger.info('Adding colour...')
        commandlist=['gdaldem', 'color-relief', '-alpha', inputfile, colourfile, outputfile]
        subprocess.call(commandlist)
        self.logger.info('Colour added.')
    
    
    def getColourTable(self):
        assert self.band is not None
        self.logger.info( "hi"+str(self.band.GetColorInterpretation()))
        return self.band.GetColorInterpretation()
    
    
    
    
    def writeProcessedRaster(self, outputfile, fileformat='GTiff', bandnr=1):
        '''
        
        Input Params:
            bandnr -- number of band
        
        '''
        self.raster_8bit = self.raster.ReadAsArray()
        assert self.raster_8bit is not None
        driver = gdal.GetDriverByName(fileformat)
        
        print('output2',outputfile)
        
        outdata = driver.Create(outputfile, self.band.XSize, self.band.YSize, bandnr, gdal.GDT_Byte)
        outdata.SetProjection( self.raster.GetProjection() )
        outdata.GetRasterBand(bandnr).SetNoDataValue(np.nan)
        outdata.SetGeoTransform(self.raster.GetGeoTransform())
        outband=outdata.GetRasterBand(bandnr)
        
        #ct = gdal.ColorTable()
        #ct.SetColorEntry(1, (0,0,102,255))      
        #ct.SetColorEntry(2, (0,255,255,255))    
        #outband.SetColorTable(ct)
        
        outband.WriteArray(self.raster_8bit)
        
        print(outband)
        
        #outband.FlushCache()
        
        #outband = None
        #outdata = None

    
if __name__ == '__main__':
    pass
    