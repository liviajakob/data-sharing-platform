'''
Queries pixel values at given coordinates
File: query_point.py

@author: livia
'''

try:
    from osgeo import gdal
except ImportError:
    import gdal
import struct
import numpy as np



def retrieve_pixel_value(geo_coord, data_source):
    """Retrieves a pixel value in a file at a given coordinate
    
    Input Parameter:
        geo_coord - two coordinates [x,y]
        data_source - the path of a datasource
    
    Returns:
        a floating-point value, nan if coordinates out of bound
        
    """
    mx, my = geo_coord[0], geo_coord[1]
    src_ds=gdal.Open(data_source) 
    gt=src_ds.GetGeoTransform()
    rb=src_ds.GetRasterBand(1)
    #Convert from map to pixel coordinates.
    #Only works for geotransforms with no rotation 
    #gt[0] is top left x, gt[1] is w-e pixel resolution
    px = int((mx - gt[0]) / gt[1]) #x pixel
    #gt[3] is top left y, gt[5] is n-s pixel resolution
    py = int((my - gt[3]) / gt[5]) #y pixel
    try:
        structval=rb.ReadRaster(px,py,1,1,buf_type=gdal.GDT_Float32) #Assumes 32 float
        intval = struct.unpack('f' , structval) #use float    
    except:
        intval=[np.nan] #give it nan value if something fails
    return intval[0]
