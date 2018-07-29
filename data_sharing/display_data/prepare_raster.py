'''
Contains all the classes to process a raster and prepare it for webdisplay

Contains:
    RasterTiler - creates raster tiles
    RasterLayerProcessor - processes raster files

@author: livia

'''

import subprocess
import gdal
import osr, math
import numpy as np

class RasterTiler(object):
    '''Class to create map tiles
    '''

    
    def createTiles(self, inputfile, outputdir, zoom="2-5"):
        '''Creates raster tiles and saves them in the output directory
        
        Input Parameter:
            inputfile (str) - input of the rasterfile to be tiled
            outputdir (str) - directory of the tiles output
            zoom (str) - zooms to compute, default is 2-5
        
        '''
        commandlist=['gdal2tiles.py', '-z', zoom, inputfile, outputdir]
        subprocess.call(commandlist)
    
    
    def calculateZoom(self, area, e0=5224000.0):
        '''area in metre
        
        Input Parameters
            area - area of a file in square meters
            e0 - area for zoomlevel 1 (in square metres)
        
        Returns
            zooms (string) - suggested zooms, e.g. 2-9
        
        '''
        length=math.sqrt(area)
        
        arr=[]
        for i in range(0,23):
            x = e0/(1.8**(i))
            arr.append(x)
        topzoom = min(range(len(arr)), key=lambda i: abs(arr[i]-length))
        bottomzoom = topzoom + 6
        
        zooms=str(topzoom)+'-'+str(bottomzoom)
        return zooms
    
    
    
##################################################  
    
class RasterLayerProcessor(object):
    '''
    Contains functions to process rasterfiles
    
    '''
    
    def __init__(self, logger):
        '''Constructor for RasterLayerProcessor
        
        Input Parameter:
            logger - a logging object
        
        '''
        self.logger = logger
        self.raster = None
        self.band = None

   
    def readFile(self, inputfile, band=1):
        '''reads a raster file with gdal
        Should be used before other functions
        
        Input Parameter:
            inputfile (str) - path of inputfile
            band (int) - number of bands, default 1
            
        '''
        self.logger.info("Starting to read raster...")
        
        try: 
            self.raster = gdal.Open(inputfile)
            assert(self.raster is not None)
        except AssertionError:
            raise IOError('file: "'+ inputfile + '" could not be opened. Check if the file exists')
        self.logger.info("Success reading raster...")
        self.band = self.raster.GetRasterBand(band) #for now I assume there is only one band


    def getStatistics(self):
        '''Returns statistics of a raster
        
        Returns:
            a dictionary containing "min", "max", "mean", "stdev"
        
        '''
        assert self.raster is not None
        stats = self.band.GetStatistics(True, True)
        statsdir = {'min' : stats[0], 'max': stats[1], 'mean' : stats[2], 'stdev' : stats[3]}
        return statsdir

    
    def getProjection(self):
        assert self.raster is not None
        '''Generates a wkt and converts it to SpatialReference object
        
        Returns:
            a SpatialReference object
        
        '''
        prj = self.raster.GetProjection()
        srs=osr.SpatialReference(wkt=prj)      
        return srs

    
    def getBoundingBoxCorners(self):
        '''Returns the bounding box corners of the raster (upper left corner and lower right corner)
        
        Returns:
            A dictionary - {"upleft": (ulx, uly), "downright": (lrx, lry)}
        
        '''
        assert self.raster is not None
        geo  = self.raster.GetGeoTransform() # get coordinates and resolution
        ulx, xres, uly, yres = geo[0], geo[1], geo[3], geo[5]
        lrx = ulx + (self.raster.RasterXSize * xres)
        lry = uly + (self.raster.RasterYSize * yres)
        #ulx, uly: upper left corner
        #lrx, lry: lower right corner
        return {'upleft': (ulx, uly), 'downright': (lrx, lry)}
    
    
    
    def getExtent(self):
        '''Returns the bounding box in minx, maxx, miny and maxy
        
        Returns:
            A dictionnary with "xmax", "ymax", "xmin" and "ymin"
        '''
        box = self.getBoundingBoxCorners()
        minXc, minYc = box['upleft'][0], box['upleft'][1]
        maxXc, maxYc = box['downright'][0], box['downright'][1] 
        if minXc > maxXc: minXc, maxXc = maxXc, minXc
        if minYc > maxYc: minYc, maxYc = maxYc, minYc
        
        return {'xmin': minXc, 'xmax': maxXc, 'ymin': minYc, 'ymax': maxYc}
    
    
    
    def getMinBoundingBox(self):
        '''Calculates a min boundingbox without cutting not Null values
        
        Returns:
            {xmin: coord, xmax: coord, ymin: coord, ymax: coord}
        
        '''
        assert self.band is not None
        grid = self.band.ReadAsArray()
        # create 1D array (x-direction) with True values where the whole column/raster of the raster is Null
        if self.band.GetNoDataValue() is None:
            xArr = np.all(np.isnan(grid), axis = 0)
            yArr = np.all(np.isnan(grid), axis = 1)
        else:
            xArr = np.all(grid==self.band.GetNoDataValue(), axis = 0)
            yArr = np.all(grid==self.band.GetNoDataValue(), axis = 1)    
            
        xContent = np.where(np.invert(xArr))
        minX, maxX = xContent[0][0]-1, xContent[0][-1]+1

        # calculate indices where yArr is False
        yContent = np.where(np.invert(yArr))
        minY, maxY = yContent[-1][0]-1, yContent[-1][-1]+1
        
        ## adjust if out of boundary
        if minX < 0: minX = 0
        if maxX > len(xArr): maxX = len(xArr)
        if minY < 0: minY = 0
        if maxY > len(yArr): maxY = len(yArr)
        
        #calculate coordinates
        geo  = self.raster.GetGeoTransform() # get corrdinates and resolution
        ulx, xres, uly, yres = geo[0], geo[1], geo[3], geo[5]
        minXc = ulx + (minX * xres)
        maxXc = ulx + (maxX * xres)
        minYc = uly + (minY * yres)
        maxYc = uly + (maxY * yres)
        
        #Flip if min and max are exchanged
        if minXc > maxXc: minXc, maxXc = maxXc, minXc
        if minYc > maxYc: minYc, maxYc = maxYc, minYc
        
        return {'xmin': minXc, 'xmax': maxXc, 'ymin': minYc, 'ymax': maxYc}


    def cutRaster(self, inputfile, outputfile, boundbox={}):
        '''Cuts the raster to a desired extent
        Default cuts the minimum boundingbox for not NaN values
        
        Input Parameter:
            inputfile (str) - the input file path
            outputfile (str) - the output file path
            boundbox (optional) - the extent it should be cropped to
        
        '''
        self.readFile(inputfile)
        # check if bounding box input is given
        if not boundbox:
            boundbox = self.getMinBoundingBox() # calculate bounding box 
        
        commandlist=['gdalwarp', '-te', str(boundbox['xmin']), str(boundbox['ymin']), str(boundbox['xmax']), str(boundbox['ymax']), '-overwrite', inputfile, outputfile]
        subprocess.call(commandlist)
        
    
    def reproject(self, inputfile, outputfile, projection):
        '''Reprojects a file to a desired projection
        
        Input Parameter:
            inputfile (str) - the input file path
            outputfile (str) - the output file path
            projection (str) - desired projection code, e.g. EPSG:3413
            
        '''
        commandlist=['gdalwarp', '-t_srs', projection, '-overwrite', inputfile, outputfile]
        subprocess.call(commandlist)
        
    
    
    def addColours(self, inputfile, outputfile, colourfile):
        '''Colours the input raster
        
        Input Parameter:
            inputfile (str) - the input file path
            outputfile (str) - the output file path
            colourfile (str) - colourfilewith structure (row): Value R G B Alpha
        
        
        '''
        self.logger.info('Adding colour...')
        commandlist=['gdaldem', 'color-relief', '-alpha', inputfile, colourfile, outputfile]
        subprocess.call(commandlist)
        self.logger.info('Colour added.')

    
    
if __name__ == '__main__':
    pass
    
