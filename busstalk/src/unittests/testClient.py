'''
Created on May 23, 2014

@author: moz
'''
import unittest

import os
import threading
parentdir = os.path.dirname(os.path.dirname( '..'))
os.sys.path.insert(0,parentdir)

import socket, sys

from bsClient import bsClient

tcpPort = 10000
srvHost = 'localhost'

def runMinimalServer():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address given on the command line
    server_address = ('', tcpPort)
    sock.bind(server_address)
    
    sock.listen(1)
    connection, client_address = sock.accept()  # @UnusedVariable
    
    try:
        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                connection.sendall(data) # just echo stuff
            else:
                return True
    finally:
        connection.close()

class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testBadConnect(self):
        ''' test connecting to non-existing server
        '''        
        self.assertRaises( IOError, bsClient, 'bogusserver', tcpPort  )
        
    
    def testGoodConnect(self):
        ''' test connecting to localhost
        '''        
        t = threading.Thread(target=runMinimalServer, name="TestClientThread" )
        t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
        t.start()
        
        self.assertRaises( IOError, bsClient, srvHost, tcpPort  )
        t.join(3)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreate']
    unittest.main()