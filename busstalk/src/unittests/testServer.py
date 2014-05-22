'''
Created on May 13, 2014

@author: moz
'''
import unittest

import os
from bsServer import bsServer
import threading
import socket
parentdir = os.path.dirname(os.path.dirname( '..'))
os.sys.path.insert(0,parentdir)

quitMessage = "QUIT"
tcpPort = 10000

class TestClass(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCreate(self):
        s = bsServer( port = tcpPort)  
        self.assertEqual( s.getConnectionCount(), 0 )
        self.assertEqual( s.getTcpPort(), tcpPort)
        
    
class TestConnection(unittest.TestCase):

    def setUp(self):
        self.bss = bsServer()
        t = threading.Thread(target=self.bss.runOnce, name="TestServerThread")
        t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
        t.start()
        pass

    def tearDown(self):
        pass

    def testConnect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', tcpPort))
        s.send( quitMessage )
        s.close()
        
        self.assertEqual( self.bss.getConnectionCount(), 1)
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()