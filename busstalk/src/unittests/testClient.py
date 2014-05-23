'''
Created on May 23, 2014

@author: moz
'''
import unittest

import os
import threading
from random import randint
parentdir = os.path.dirname(os.path.dirname( '..'))
os.sys.path.insert(0,parentdir)

import socket, sys

from bsClient import bsClient

tcpPort = randint(10000,11000)
srvHost = 'localhost'

def runMinimalServer( ReturnData = ("WELCOME\n", )  ):
    ''' create a server and return the strings from the array, one line at the time 
        as response to (un-parsed) received data
    '''
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address given on the command line
    server_address = ('', tcpPort)
    sock.bind(server_address)
    
    sock.listen(1)
    connection, client_address = sock.accept()  # @UnusedVariable
    
    for retval in ReturnData:
        # fetch data while available
        while True:
            data = connection.recv(16)
            print >> sys.stderr, "recv: %s"%data
            if data[-1] != '\n':
                continue
            else:
                print >> sys.stderr, "sending: %s" %retval
                connection.sendall(retval) # just echo stuff
                break
            
    connection.close()
    print >> sys.stderr, "done"

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
         
        c = bsClient( srvHost, tcpPort  )  # @UnusedVariable
        t.join(3)
         
     
#     def testReturnVal(self):
#         ''' test connecting to localhost
#         '''        
#         t = threading.Thread(target=runMinimalServer, name="TestClientThread" )
#         t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
#         t.start()
#         
#         self.assertRaises( IOError, bsClient, srvHost, tcpPort  )
#         t.join(3)
#         

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreate']
    unittest.main()