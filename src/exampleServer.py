'''
Created on Sep 5, 2014

@author: moz
'''
from i2cDevices import i2cDevice
from bsServer import bsServer

class device(object):
    '''
    classdocs
    '''
    def __init__(self):
        # Init i2c device class
        self._mcp = i2cDevice( BusToUse = 1, i2cAddr = 0x20 )
        self._mcp.writeByte( 0x00, 0x00 ) # set bank A to output on all pins

    def getName(self):
        return "MCF"

    def setAddress(self, addr, val ):
        self._mcp.writeByte( addr, val )
        return True
    
    def getAddress(self, addr ):
        val = self._mcp.readByte( addr )
        return val

if __name__ == '__main__':
    srv = bsServer( deviceList = device(), port = 10000)
    srv.start()