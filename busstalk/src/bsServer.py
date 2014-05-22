'''
Created on May 13, 2014

@author: moz

Most of this comes from http://pymotw.com/2/socket/tcp.html
'''

import socket
import sys


class bsServer(object):
    '''
    classdocs
    '''

    def __init__(self, port = 10000):
        '''
        Constructor
        '''
        self._ConnectionCount = 0
        self._tcpPort = port
    
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the address given on the command line
        server_address = ('', self._tcpPort)
        self.sock.bind(server_address)
        print >>sys.stderr, 'Starting BS server up on %s port %s' % self.sock.getsockname()
        
        
    def runOnce(self):
        ''' the main function to handle incoming data
        '''
        self.sock.listen(1)
        
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = self.sock.accept()
        self._ConnectionCount += 1
        try:
            print >>sys.stderr, 'client connected:', client_address
            while True:
                data = connection.recv(16)
                print >>sys.stderr, 'received "%s"' % data
                if data:
                    connection.sendall(data) # just echo stuff
                else:
                    return True
        finally:
            connection.close()
            
    def runMultiple(self, count = 1):
        ''' handles multiple consecutive connections
        '''
        while count > 0:
            if not self.runOnce():
                return False
            
            count -= 1
        
    def start(self):
        ''' server will sit and wait for connection from client
            and then process it.
        '''
        self.sock.listen(1)
        
        while True:
            if not self.runOnce():
                break

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
                