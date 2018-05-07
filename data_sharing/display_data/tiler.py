'''

@author: livia
'''

import subprocess


class Tiler(object):
    '''
    Creates tiles
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    
    def createTiles(self, inputfile, outputdir, colours = None, zoom="0-5"):
        print(inputfile)
        commandlist=['gdal2tiles.py', '-z', zoom, '-p', 'raster', inputfile, outputdir]
        #command = " ".join(commandlist)
        print(commandlist)
        subprocess.call(commandlist)
    
    
    
class LayerProcessor(object):
    '''
    Creates Layer entries
    '''
    
    
    
    def __init__(self, database):
        '''
        Constructor
        '''
        self.database = database
        
        
    
    def layerExists(self):
        return False
    
    
    def layerUpdated(self):
        pass
   
   
    

if __name__ == '__main__':
    
    pass
    