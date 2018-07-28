'''
Manages the ingestion rollback
File: rollback.py

Contains:
    Singleton       – metaclass for the Singleton pattern implementation
    Rollback        – a class storing and executing rollback commands 

@author: livia
'''

class Singleton(type):
    '''Metaclass to create Singleton classes
    
    _instances – saves the instances of classes
    
    '''  
    # saves the instances of the classes
    _instances = {}
    
    def __call__(self, *args, **kwargs):
        '''Returns the instance if it already exists, creates a new instance if it doesn't exist
        
        Returns:
            an instance of a the class
        
        '''
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]



class Rollback(metaclass=Singleton):
    '''
    Class acting like a stack
    can be used to store rollback commands and execute them in reversed order
    
    '''


    def __init__(self):
        '''Constructor of Rollback
        
        Input Parameter:
            logger – a python logging object
        
        '''
        self._commands = []
        
        
    def addCommand(self, command, params={}):
        '''Adds a command to the rollback
        
        Input parameter:
            command – a command function
            params – (default: {}) a keyword dictionary with the command function parameters
        
        '''
        newCommand = [command, params]
        self._commands.append(newCommand)
        
        
        
    def rollback(self):
        '''Executes all the saved commands, starting with the last added command (lick a stack)
        
        '''
        for cmd in reversed(self._commands):
            print(cmd)
            cmd[0](**cmd[1])
        
    def getCommands(self):
        '''Getter for commands
        
        Returns:
            commands (list) – a list of the saved commands
        '''
        return self._commands

