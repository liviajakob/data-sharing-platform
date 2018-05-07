'''

@author: livia
'''
import unittest
import logging
from display_data import Rollback


class RollbackTest(unittest.TestCase):
    '''Tests the functionality of the Rollback class'''

    def setUp(self):
        logging.basicConfig(level=logging.NOTSET) #NOTSET gives all the levels, e.g. INFO only .info
        logger = logging.getLogger(__name__)
        # add handler file
        handler = logging.FileHandler('test_logger.log')
        handler.setLevel(logging.INFO)
        # add the handlers to the logger
        logger.addHandler(handler)
        #create the rollback
        self.rl = Rollback(logger)

    def test_addCommand(self):
        '''Tests if commands are added'''
        hlp = Helper()
        cmd = [hlp.change, {'val1': 1, 'val2': 2}]
        self.rl.addCommand(cmd[0], cmd[1])
        self.assertEqual(self.rl.getCommands()[0], cmd, "Command not added properly")
        
        
    def test_rollback(self):
        '''Tests the rollback, tests if it's been reversed'''
        hlp = Helper()
        cmd1 = [hlp.change, {'val1': 1, 'val2': 2}]
        self.rl.addCommand(cmd1[0], cmd1[1])
        cmd2 = [hlp.change, {'val1': 3, 'val2': 4}]
        self.rl.addCommand(cmd2[0], cmd2[1])
        self.assertEqual(len(self.rl.getCommands()), 2, "Did not insert all commands")
        self.rl.rollback()
        self.assertNotEqual(hlp.testvalue1, 3, "Rollback has not been reversed")
        self.assertEqual(hlp.testvalue1, 1, "Command has not been properly executed")
        self.assertEqual(hlp.testvalue2, 2, "Command has not been properly executed")
        
        
    
    
class Helper(object):
    '''Helper class for the rollback test'''
    
    def __init__(self):
        self.testvalue1=0
        self.testvalue2=0
    
    def change(self, val1, val2):
        self.testvalue1 = val1
        self.testvalue2 = val2
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()