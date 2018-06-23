'''
Created on 22 Jun 2018

@author: livia
'''

import os

class ColourMaker(object):
    '''
    classdocs
    '''


    def __init__(self, output):
        '''
        Constructor
        '''
        self.output = output
        
    
    
    def computeColours(self, inpcolours, min_val, max_val):
        
        nr_of_values = 60
        arr = []
        for i in range(60):
            val=(i/(abs(max_val-min_val)))*nr_of_values
            arr.append(val)
            
        
        print(arr)
        
        
        
    def destroy(self):
        '''Removes the colourfile if it exists'''
        try:
            os.remove(self.output)
        except:
            pass
        
        
if __name__ == "__main__":
    col = ColourMaker('hi')
    col.computeColours('', 60, 1)