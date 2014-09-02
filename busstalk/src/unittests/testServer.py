'''
Created on May 13, 2014

@author: moz
'''
import unittest

import os, time
from bsServer import bsServer
import threading
import socket
from random import randint
parentdir = os.path.dirname(os.path.dirname( '..'))
os.sys.path.insert(0,parentdir)

firstMessage  = "GREETINGS\n"
firstMessage2 = "GREETINGS\r\n"
firstReply = "WELCOME\n"
testCount = 3

class TestServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCreate(self):
        ''' test simple class instatiation '''
        tcpPort = randint(10000,11000)
        s = bsServer( port = tcpPort)  
        self.assertEqual( s.getConnectionCount(), 0 )
        self.assertEqual( s.getTcpPort(), tcpPort)
        
    def testConnect(self):
        ''' test tcp connection '''
        tcpPort = randint(10000,11000)        
        bss = bsServer(port = tcpPort)  
        t = threading.Thread(target=bss.runOnce, name="TestServerThread")
        t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
        t.start()
        time.sleep(0.1)
 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(('localhost', tcpPort))
        s.send( firstMessage )
        retval = s.recv(50)
        s.close()
         
        t.join(3)
        self.assertEqual( bss.getConnectionCount(), 1)
        self.assertEqual( retval, firstReply)
        pass
  
    def testConnectWithCarriageReturn(self):
        ''' test tcp connection '''
        tcpPort = randint(10000,11000)        
        bss = bsServer(port = tcpPort)  
        t = threading.Thread(target=bss.runOnce, name="TestServerThread")
        t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
        t.start()
        time.sleep(0.1)
 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(('localhost', tcpPort))
        s.send( firstMessage2 )
        retval = s.recv( 50)
        s.close()
         
        t.join(3)
        self.assertEqual( bss.getConnectionCount(), 1)
        self.assertEqual( retval, firstReply)
        pass
  
    def testMultipleConnect(self):
        tcpPort = randint(10000,11000)
        bss = bsServer(port = tcpPort)  
        t = threading.Thread(target=bss.runMultiple, name="TestServerThread", args=(testCount,) )
        t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
        t.start()
        time.sleep(0.1)
           
        for i in range(0, testCount ):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(30)
            s.connect(('localhost', tcpPort))
            s.send( firstMessage )
            #s.send( "connection %d\n"%i )
            time.sleep(0.1)
            s.shutdown( socket.SHUT_RDWR)
            time.sleep(0.1)
            s.close()
          
        t.join(3)
        #t.join()
        self.assertEqual( bss.getConnectionCount(), testCount )
        pass
 
    def testQuit(self):
        tcpPort = randint(10000,11000)
        bss = bsServer(port = tcpPort)  
        t = threading.Thread(target=bss.start, name="TestServerThread" )
        t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
        t.start()
        time.sleep(0.1)
  
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(50)
        s.connect(('localhost', tcpPort))
          
        # doing greeting
        s.send( "GREETINGS\n" )
        fromSrv = ''
        while True:
            data = s.recv(16)
            self.assertTrue(data)
            fromSrv += data
            if len(fromSrv) > 1 and fromSrv[-1] == '\n':
                break
        self.assertEqual( fromSrv, 'WELCOME\n')
  
        s.send( "DEVICES\n" )        
        fromSrv = ''
        while True:
            data = s.recv(16)
            self.assertTrue(data)
            fromSrv += data
            if len(fromSrv) > 1 and fromSrv[-1] == '\n':
                break
        self.assertEqual( fromSrv, 'OK DEVICES EEPROM LED\n')
          
        s.close()
      
        t.join(3)
        pass
    
        
# class TestConnection(unittest.TestCase):
# 
#     def setUp(self):
#         self.tcpPort = randint(10000,11000)
#         bss = bsServer(port = self.tcpPort)  
#         self.t = threading.Thread(target=bss.start, name="TestServerThread" )
#         self.t.daemon = False  # thread dies when main thread (only non-daemon thread) exits.
#         self.t.start()
#         time.sleep(0.1)
# 
#     def tearDown(self):
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect(('localhost', self.tcpPort))
#         s.send( firstMessage )
#         s.close()
# 
#     def testQuit(self):
#         
#         pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()