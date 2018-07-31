'''
Unittests for the Rollback class
File: test_rollback.py

@author: livia
'''
import unittest
from display_data import Rollback


class RollbackTest(unittest.TestCase):
    '''Tests the functionality of the Rollback class'''

    def setUp(self):
        pass

    def test_addCommand(self):
        '''Tests if command is added'''
        rl = Rollback()
        hlp = Helper()
        cmd = [hlp.change, {'val1': 1, 'val2': 2}]
        rl.addCommand(cmd[0], cmd[1])
        self.assertEqual(rl.getCommands()[0], cmd, "Command not added")
        
        
    def test_rollback(self):
        '''Tests the rollback, tests if it's been reversed'''
        rl = Rollback()
        hlp = Helper()
        cmd1 = [hlp.change, {'val1': 1, 'val2': 2}]
        rl.addCommand(cmd1[0], cmd1[1])
        cmd2 = [hlp.change, {'val1': 3, 'val2': 4}]
        rl.addCommand(cmd2[0], cmd2[1])
        self.assertEqual(len(rl.getCommands()), 3, "Did not insert all commands")
        rl.rollback()
        self.assertNotEqual(hlp.testvalue1, 3, "Rollback has not been reversed")
        self.assertEqual(hlp.testvalue1, 1, "Command has not been properly executed")
        self.assertEqual(hlp.testvalue2, 2, "Command has not been properly executed")
        
       
    def test_singleton(self):
        '''Tests the singleton pattern'''
        rl1 = Rollback()
        rl2 = Rollback()
        self.assertEqual(rl1, rl2, "Singleton pattern not working, should be equal")
    
    
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