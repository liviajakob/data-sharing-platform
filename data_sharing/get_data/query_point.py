'''
Created on 11 Jun 2018

@author: livia
'''


import rasterio
from display_data.system_configuration import ConfigSystem



lons = [-122.265373, -122.429139, -68.123095]
lats = [37.873090, 37.783640, 44.981935]


def queryPoint():
    lons = [-122.265373, -122.429139, -68.123095]
    lats = [37.873090, 37.783640, 44.981935]
    conf=ConfigSystem()
    fname = conf.getLayerRawFile('dem', 14)
    print(fname)
    with rasterio.open(fname) as src:
        for val in src.sample(zip(lons, lats)):
            print (val)


if __name__ == '__main__':
    queryPoint()
    pass