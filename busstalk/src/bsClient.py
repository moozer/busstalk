'''
Created on May 13, 2014

@author: moz

Most of this comes from http://pymotw.com/2/socket/tcp.html
'''

import socket
import sys




class bsClient(object):
    '''
    classdocs
    '''

    def __init__(self, remoteServer, remotePort = 10000 ):
        '''
        Constructor
        '''
        
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect the socket to the port on the server given by the caller
        self.server_address = (remoteServer, remotePort )
        
        print >>sys.stderr, 'Client will connect to %s port %s' % self.server_address

        self.sock.connect(self.server_address)
        
        try:
            
            message = 'This is the message.  It will be repeated.'
            print >>sys.stderr, 'sending "%s"' % message
            self.sock.sendall(message)
        
            amount_received = 0
            amount_expected = len(message)
            while amount_received < amount_expected:
                data = self.sock.recv(16)
                amount_received += len(data)
                print >>sys.stderr, 'received "%s"' % data
        
        finally:
            self.sock.close()
            
# the program starts from here
if __name__ == "__main__":
    client = bsClient( "localhost" )

