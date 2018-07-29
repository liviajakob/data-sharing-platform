'''
Responsible for computing concrete colourfiles from colour templates
File: compute_colours.py

Contains:
    ColourFactory          - Factory class with factory method to create ColourMakers
    ColourMaker            - Interface for concrete ColourMakers
    LinearColourMaker      - Creates a linear colourfile from min, max values
    CentredColourMaker     - Creates a centred colourfile from min, max values

@author: livia
'''

import os, abc
import numpy as np


class ColourFactory():
    '''Factory class with factory method to create ColourMakers
    
    '''
    
    def get_colourmaker(self, colourmaker_type, inputfile, outputpath):
        '''Factory class to create a ColourMaker
        
        Input Parameter:
            colourmaker_type (String) - the type of the colourmaker which should be created, e.g. 'linear' or 'centred'
            inputfile (String) - path of the template colourfile
            outputfile (String) - path of where the computed colourfile should be saved
        
        Returns:
            colourmaker object inheriting from the ColourMaker class
        
        '''
        if colourmaker_type == 'centred':
            return CentredColourMaker(inputfile, outputpath)
        elif colourmaker_type == 'linear':
            return LinearColourMaker(inputfile, outputpath)


########################


class ColourMaker(abc.ABC):
    '''Colour maker interface
    Responsible for making colour tables in GDAL format
    
    Children must include:
        compute_colours()
    
    '''

    def __init__(self, inputfile, outputpath):
        '''Constructor of ColourMaker
        
        Input Parameter:
            inputfile (String) - path of the template colourfile
            outputfile (String) - path of where the computed colourfile should be saved
        
        '''
        self.col_output = outputpath
        self.col_input = inputfile



    def get_col_output(self):
        '''Returns the colour output file path
        
        Returns:
            filepath (String) - the colour output file path
        '''
        return self.col_output


    def get_col_input(self):
        '''Returns the colour input file path
        
        Returns:
            filepath (String) - the colour input file path
        '''
        return self.col_input

    
    @abc.abstractmethod
    def computeColours(self, min_val, max_val):
        '''Abstract method that has to be implemented by child classes
    
        Input Parameter:
            min_val (int/float) - minimum saturation value
            max_val (int/float) - maximum saturation value
    
        Should compute and create a colourfile with min_values and max_values as saturation values
        '''
        pass
    
    
    def writeFile(self, values):
        '''Writes values and colours into an outputfile
        
        Input Parameter:
            values (numpy.array) - a 2-dimensional array with the computed values and colours
        
        '''
        colours = np.genfromtxt(fname=self.col_input) #read file into array
        output = np.concatenate((values, colours), axis=1) # concatenate colours and values
        np.savetxt(self.col_output, output, fmt='%1.3f') # save output in file
        self.appendTransparentLine() # add line to make null values transparent
    
    
       
    def calculateLinearValues(self, nr_of_values, min_val, max_val):
        '''Calculates a linear sequence of n values between a minimum and a maximum value
        
        Input Parameter:
            nr_of_values (int) - Number of output values that should be calculated
            min_val (int/float) - minimum value
            max_val (int/float) - maximum value
        
        Returns
            values (list) - a list of the requested values 
        '''
        vals = []
        for i in range(nr_of_values):
            val=(min_val+((i/(nr_of_values-1))*(abs(max_val-min_val))))
            vals.append(val)
        return vals
      
       
    def appendTransparentLine(self):
        '''Adds a line for transparent values to the colourfile
        Can be used to colour null values transparent
        
        '''
        with open(self.col_output, 'a') as file:
            file.write('nan 0 0 0 0\n')
        
     
       
    def file_len(self):
        '''Returns number of rows in a file
        
        Returns:
            number (int) - the number of rows
        '''
        return sum(1 for line in open(self.col_input))
    
        
    def destroy(self):
        '''Removes the generated colourfile
        No exception raised if file does not exists
        
        '''
        try:
            os.remove(self.col_output)
        except:
            pass # do nothing


########################

class LinearColourMaker(ColourMaker):
    '''Creates linear colourfiles from a template
    
    '''
    
    def computeColours(self, min_val, max_val):
        '''Implementation of abstract method of parent class
        Computes the values linear
        
        Input Parameter:
            min_val (int/float) - minimum saturation value
            max_val (int/float) - maximum saturation value
        
        '''
        nr_of_values = self.file_len()
        vals = self.calculateLinearValues(nr_of_values, min_val, max_val)
        values= np.reshape(vals, (nr_of_values,1)) # reshape values
        self.writeFile(values)




########################
    
class CentredColourMaker(ColourMaker):
    '''Makes colourfiles centred at 0
    
    Assumes that input colourfile is centred
    '''
    
    
    def computeColours(self, min_val, max_val):
        '''Implementation of abstract method of parent class
        Computes the values centred around 0
        
        Input Parameter:
            min_val (int/float) - minimum saturation value
            max_val (int/float) - maximum saturation value
        
        '''    
        assert min_val < 0
        assert max_val > 0
        
        nr_of_values = self.file_len()
        nr = round(nr_of_values/2)
        nr2 = (nr_of_values+1) - nr #ensures that length is right
        
        vals1=self.calculateLinearValues(nr, min_val, 0)
        vals2=self.calculateLinearValues(nr2, 0, max_val)

        vals = vals1+vals2[1:]
      
        values= np.reshape(vals, (nr_of_values,1)) # reshape values
        self.writeFile(values)


    
    