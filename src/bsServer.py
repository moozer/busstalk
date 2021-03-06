'''
Created on May 13, 2014

@author: moz

Most of this comes from http://pymotw.com/2/socket/tcp.html
'''

import socket
import sys
import time
from chatMod import chatMod


class bsServer(object):
    '''
    classdocs
    '''

    def __init__(self, deviceList, port = 10000):
        '''
        Constructor
        '''
        self._ConnectionCount = 0
        self._tcpPort = port
        self._deviceList = deviceList
    
        # Create a TCP/IP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the address given on the command line
        server_address = ('', self._tcpPort)
        self._sock.bind(server_address)
        print >>sys.stderr, 'Starting BS server up on %s port %s' % self._sock.getsockname()
        
    def _send(self, text ): 
        ''' send the specified text - newline is automaticly appended, if needed
        '''
        if text[-1] != '\n':
            text += '\n'
        self._curConnection.sendall( text ) 
        
    def _receive( self, timeoutcount = 20, waittime = 0.1 ):
        ''' Merges all received data until newline is received.
        '''
        # TODO: what happens if newline is not the last char?
        retval = ''
        while True:
            data = self._curConnection.recv( 16 )
            
            # if no data, just try again
            if len(data) > 0:
                retval += data
                
                # if newline at the end, we have a command
                if retval[-1] == '\n':
                    break

            else:
                time.sleep( waittime )
                timeoutcount -= 1
                #print >> sys.stderr, "(%d) waiting: %d"%(self._tcpPort, timeoutcount)
                
            # if timeout
            if timeoutcount < 1:
                return "TIMEOUT"
            
        return retval.strip()
    

    
    def runOnce(self ):
        ''' the main function to handle incoming data
        '''
        self.runMultiple(1)
#         self._sock.listen(1)
#         command = ""
#         
#         print >>sys.stderr, 'waiting for a connection'
#         connection, client_address = self._sock.accept()
#         print >>sys.stderr, 'client connected:', client_address
#         self._ConnectionCount += 1
#         try:
#             command = self._receive()
#             return self._parse(command)
#         except IOError, e: 
#             print >> sys.stderr, "Error caught receiving data so closing connection: %s"%e
#         finally:
#             connection.shutdown()
#             connection.close()
            
    def runMultiple(self, count = 1, runForever = False):
        ''' handles multiple consecutive connections
        '''
        self._sock.listen(1)
        command = ""
        notQuit = True
        c = chatMod( self._deviceList )
        
        try:
            print >>sys.stderr, '(%d) waiting for a connection'%self._tcpPort
            
            self._curConnection, client_address = self._sock.accept()
            print >>sys.stderr, "(%d) client connected: %s"%(self._tcpPort, client_address)
        
            while runForever or count > 0:
                self._ConnectionCount += 1
                count -= 1
                try:
                    command = self._receive()
                    print >> sys.stderr, "command: %s"%command
                    notQuit, sendString = c.parse(command)
                    self._send( sendString)
                    if not notQuit:
                        break                
                except IOError, e: 
                    print >> sys.stderr, "(%d) IOError caught receiving/sending data - closing connection: %s"%(self._tcpPort, e)
                    break           

        finally:
            print >>sys.stderr, "(%d) shutdown and close"%self._tcpPort
            #self._curConnection.shutdown(socket.SHUT_RDWR)
            self._curConnection.close()
            
        if not notQuit:
            return
        
        # TODO: this is bad
        if count > 0:
            self.runMultiple(count, runForever)
        
    def start(self):
        ''' server will sit and wait for connection from client
            and then process it.
        '''
        self.runMultiple( count = 0, runForever=True)
        print >> sys.stderr, "Shutdown as per requested"

    # --- 
    # getters 
    # ---
    def getConnectionCount(self):
        return self._ConnectionCount

    def getTcpPort(self):
        return self._tcpPort
          

# the program starts from here
if __name__ == "__main__":
    srv = bsServer()
    srv.start()
                