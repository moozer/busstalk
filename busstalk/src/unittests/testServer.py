'''
Created on May 13, 2014

@author: moz
'''
import unittest

import os
from bsServer import bsServer
parentdir = os.path.dirname(os.path.dirname( '..'))
os.sys.path.insert(0,parentdir)



class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testCreate(self):
        s = bsServer()
        
        self.assertEqual( s.getConnectionCount(), 0, "initial connection must be 0" )
        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()