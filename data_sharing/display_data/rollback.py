'''

@author: livia
'''
import logging

class Rollback(object):
    '''
    Rollback the ingestion;
    '''


    def __init__(self, logger):
        '''
        Constructor
        '''
        assert(isinstance(logger, logging.Logger))
        self.logger = logger
        self._commands = []
        
        
    def addCommand(self, command, params={}):
        newCommand = [command, params]
        self._commands.append(newCommand)
        
        
        
    def rollback(self):
        self.logger.info("Starting rollback...")
        for cmd in reversed(self._commands):
            cmd[0](**cmd[1])
        self.logger.info("Finished rollback...")
        
    def getCommands(self):
        return self._commands
