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
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect the socket to the port on the server given by the caller
        self.server_address = (remoteServer, remotePort )
        
        print >>sys.stderr, 'Client will connect to %s port %s' % self.server_address

        self._sock.connect(self.server_address)

        self._send( 'GREETINGS' )
        if not self._receive().split(' ')[0] == 'WELCOME':
            raise IOError( 'Unknown response' )
    
    def __enter__(self):
        return self
    
    def __exit__(self, errortype, value, traceback): 
        print >> sys.stderr, "Closing socket"
        self._sock.shutdown(socket.SHUT_RDWR)
        while True:
            data = self._sock.recv(16)
            if not data:
                break
        self._sock.close()
    
    def _send(self, text ): 
        ''' send the specified text - newline is automaticly appended, if needed
        '''
        if text[-1] != '\n':
            text += '\n'
        self._sock.sendall( text )        

    def _receive(self):
        ''' Merges all received data until newline is received.
        '''
        # TODO: what happens if newline is not the last char?
        retval = ''
        while True:
            data = self._sock.recv( 16 )
            retval += data
            if retval[-1] == '\n':
                break
                
        return retval[:-1]

    def _sendCommand(self, command ):
        self._send(command)
        data = self._receive().split(' ')
        
        # first word is success or not
        result = data.pop(0)
        if result != "OK":
            raise IOError( "Command '%s' failed: %d"%(command, data))
        
        # next word is the command echo
        cmdEcho = data.pop(0)
        if cmdEcho != command:
            raise IOError( "Command echo failed: Got '%s' exspected '%s'"%(cmdEcho, command))
        
        # the rest is the result
        return data

    def getDevices(self):
        ''' Send a request for the list of devices
            ie. send "DEVICES" command
        '''
        cmd = "DEVICES"
        retval = self._sendCommand(cmd)
        return retval
        
            
# the program starts from here
if __name__ == "__main__":
    client = bsClient( "localhost" )

