'''
Created on 22 Jun 2018

@author: livia
'''

import os
import numpy as np

class ColourMaker(object):
    '''
    Responsible for making colour tables in GDAL format
    
    '''

    def __init__(self, inputfile, outputpath):
        '''
        Constructor
        '''
        self.col_output = outputpath
        self.col_input = inputfile

    def get_col_output(self):
        return self.__col_output


    def get_col_input(self):
        return self.__col_input


    def set_col_output(self, value):
        self.__col_output = value


    def set_col_input(self, value):
        self.__col_input = value
    
    
    def computeColours(self, min_val, max_val):
        
        nr_of_values = self.file_len()

        
        
        vals = self.calculateValues(nr_of_values, min_val, max_val)
        values= np.reshape(vals, (nr_of_values,1)) # reshape values
        self.writeFile(values)
    
    
    def writeFile(self, values):
        '''Writes values into an outputfile'''
        colours = np.genfromtxt(fname=self.col_input) #read file into array
        output = np.concatenate((values, colours), axis=1) # concatenate colours and values
        np.savetxt(self.col_output, output, fmt='%1.3f') # save output in file
        self.appendTransparentLine() # add line to make null values transparent
    
    
       
    def calculateValues(self, nr_of_values, min_val, max_val):
        '''Calculates a linear sequence of n values between a minimum and a maximum value'''
        vals = []
        for i in range(nr_of_values):
            val=(min_val+((i/(nr_of_values-1))*(abs(max_val-min_val))))
            vals.append(val)
        return vals
      
    
       
    def appendTransparentLine(self):
        '''Adds a line for transparent null values colour to the colourfile'''
        with open(self.col_output, 'a') as file:
            file.write('nan 0 0 0 0\n')
        
     
       
    def file_len(self):
        '''Returns number of rows in a file'''
        return sum(1 for line in open(self.col_input))
    
        
    def destroy(self):
        '''Removes the generated colourfile (if it exists)'''
        try:
            os.remove(self.col_output)
        except:
            pass





    
class CentredColourMaker(ColourMaker):
    '''Makes colourfiles centred at 0
    
    Assumes that input colourfile is centred
    '''
    
    
    def computeColours(self, min_val, max_val):
        '''Overrides parent method
        
        Computes the values centred around 0
        '''
        
        assert min_val < 0
        assert max_val > 0
        
        nr_of_values = self.file_len()
        nr = round(nr_of_values/2)
        nr2 = (nr_of_values+1) - nr #ensures that length is right
        
        vals1=self.calculateValues(nr, min_val, 0)
        vals2=self.calculateValues(nr2, 0, max_val)

        vals = vals1+vals2[1:]

        
        values= np.reshape(vals, (nr_of_values,1)) # reshape values
        self.writeFile(values)



        
    
        
'''if __name__ == "__main__":
    
    inp = '/Users/livia/msc_dissertation/CODE/data_sharing/data/input/colourfiles/rate_colours.txt'
    out = '/Users/livia/msc_dissertation/CODE/data_sharing/data/input/colourfiles/example.txt'
    col = CentredColourMaker(inp, out)
    col.computeColours(-1, 1)'''

    
    
    

    
    