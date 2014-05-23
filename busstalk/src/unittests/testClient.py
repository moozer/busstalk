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

import socket, sys, time

from bsClient import bsClient

srvHost = 'localhost'
srvErrorMsg = 'ERROR'

def runMinimalServer( tcpPort, ReturnData = ("WELCOME\n", )  ):
    ''' create a server and return the strings from the array, one line at the time 
        as response to (un-parsed) received data
        NB: Remember newlines!
    '''
    
    print >> sys.stderr, "%s: starting"%(threading.current_thread().name )
        
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address given on the command line
    server_address = ('', tcpPort)
    
    try:
        sock.bind(server_address)
    except IOError, e:
        print >> sys.stderr, "%s: Not creating server!! %s"%(threading.current_thread().name, e.message)
        return
        
    
    sock.listen(1)
    connection, client_address = sock.accept()  # @UnusedVariable
    
    for retval in ReturnData:
        # fetch data while available
        while True:
            data = connection.recv(16)
            if len(data) < 1:
                print >> sys.stderr, "%s: zero data"%threading.current_thread().name
                connection.sendall( srvErrorMsg + " zero data received\n")
                break
            print >> sys.stderr, "%s: recv: %s"%(threading.current_thread().name, data)
            if len(data) < 1 or data[-1] != '\n':
                continue
            else:
                print >> sys.stderr, "%s: sending: %s" %(threading.current_thread().name, retval)
                connection.sendall(retval) # just echo stuff
                break
            
    connection.shutdown( socket.SHUT_RDWR )
    connection.close()
    print >> sys.stderr, "%s: done"%threading.current_thread().name

class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testBadConnect(self):
        ''' test connecting to non-existing server
        '''        
        tcpPort = randint(10000,11000)
        self.assertRaises( IOError, bsClient, 'bogusserver', tcpPort  )
        
    
    def testGoodConnect(self):
        ''' test connecting to localhost
        '''        
        tcpPort = randint(10000,11000)

        t = threading.Thread(target=runMinimalServer, name="__testGoodConnect", args=(tcpPort,) )
        t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
        t.start()
        time.sleep(0.1)
         
        with bsClient( srvHost, tcpPort  ) as c:  # @UnusedVariable
            pass
        
        t.join(3)
         
     
    def testGetDevices(self):
        ''' test connecting to localhost
        '''        
        tcpPort = randint(10000,11000)
        
        t = threading.Thread(target=runMinimalServer, 
                             name="__testGetDevices", args=(tcpPort, ('WELCOME\n', 'OK DEVICES EEPROM LED\n'), ) )
        t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
        t.start()
        time.sleep(0.1)
          
        with bsClient( srvHost, tcpPort  ) as c:  # @UnusedVariable
            devs = c.getDevices()
            self.assertEqual( devs, ['EEPROM', 'LED'])
 
        t.join(3)
          

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreate']
    unittest.main()