'''
Created on 11 Jun 2018

@author: livia
'''



from display_data.system_configuration import ConfigSystem
import gdal
import struct
import numpy as np



def retrieve_pixel_value(geo_coord, data_source):
    """Return floating-point value that corresponds to given point."""
    print(data_source)
    mx, my = geo_coord[0], geo_coord[1]
    src_ds=gdal.Open(data_source) 
    gt=src_ds.GetGeoTransform()
    rb=src_ds.GetRasterBand(1)
    #Convert from map to pixel coordinates.
    #Only works for geotransforms with no rotation.
    px = int((mx - gt[0]) / gt[1]) #x pixel
    py = int((my - gt[3]) / gt[5]) #y pixel
    
    try:
        structval=rb.ReadRaster(px,py,1,1,buf_type=gdal.GDT_Float32) #Assumes 32 float
        intval = struct.unpack('f' , structval) #use float    
    except:
        intval=[np.nan]
    return intval[0]


if __name__ == '__main__':
    #queryPoint()
    conf=ConfigSystem()
    fname = conf.getLayerTimeRawFile('dem', 17)
    coords=[-102834.5, -2151176.688]
    coords2=[34,235]
    retrieve_pixel_value(coords2, fname)
    pass