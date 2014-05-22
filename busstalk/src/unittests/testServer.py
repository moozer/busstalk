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
testCount = 5

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
        pass

    def tearDown(self):
        pass

    def testConnect(self):
        bss = bsServer(port = tcpPort)  
        t = threading.Thread(target=bss.runOnce, name="TestServerThread")
        t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
        t.start()
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', tcpPort))
        s.send( quitMessage )
        s.close()
        
        t.join(3)
        self.assertEqual( bss.getConnectionCount(), 1)
        pass

    def testMultipleConnect(self):
        bss = bsServer(port = tcpPort)  
        t = threading.Thread(target=bss.runMultiple, name="TestServerThread", args=(testCount,) )
        t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
        t.start()
         
        for i in range(0, testCount ):  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', tcpPort))
            s.send( "connection %d"%i )
            s.close()
        
        t.join(3)
        self.assertEqual( bss.getConnectionCount(), testCount )
        pass



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()