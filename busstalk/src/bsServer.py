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

    def __init__(self):
        '''
        Constructor
        '''
        self._ConnectionCount = 0
    
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the address given on the command line
        server_address = ('', 10000)
        self.sock.bind(server_address)
        print >>sys.stderr, 'Starting BS server up on %s port %s' % self.sock.getsockname()
        
    def start(self):
        ''' server will sit and wait for connection from client
            and then process it.
        '''
        self.sock.listen(1)
        
        while True:
            print >>sys.stderr, 'waiting for a connection'
            connection, client_address = self.sock.accept()
            try:
                print >>sys.stderr, 'client connected:', client_address
                while True:
                    data = connection.recv(16)
                    print >>sys.stderr, 'received "%s"' % data
                    if data:
                        connection.sendall(data)
                    else:
                        break
            finally:
                connection.close()

    
    def getConnectionCount(self):
        return self._ConnectionCount
    
    
                

# the program starts from here
if __name__ == "__main__":
   srv = bsServer()
   srv.start()
                