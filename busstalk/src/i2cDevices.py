'''
Created on May 13, 2014

@author: moz
'''

import smbus
import time, sys

class i2cDevice(object):
    '''
    classdocs
    '''


    def __init__(self, BusToUse, i2cAddr ):
        '''
        Constructor
        @param BusToUse: 0 or 1
        @param i2cAddr: address of device
        '''
        self.bus = smbus.SMBus(BusToUse)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
        self.i2cAddr = i2cAddr      #7 bit address (will be left shifted to add the read write bit)
        
    def writeRandom(self, PtrOffset):        
        ''' writes a random integer to the memory specified by PtrOffset
            returns the integer written
        '''
        from random import randint
        SomeData = randint( 0, 0xff )
        
        print >> sys.stderr, "set area 0x%x to 0x%x"%(PtrOffset, SomeData )
        self.bus.write_i2c_block_data( self.i2cAddr, PtrOffset, [SomeData, SomeData] )
        
        return SomeData

    def writeByte(self, PtrOffset, dataByte):
        ''' writes a single byte to specified register
        '''
        print >> sys.stderr, "set area 0x%x to 0x%x"%(PtrOffset, dataByte )
        self.bus.write_byte_data( self.i2cAddr, PtrOffset, dataByte  )
        return dataByte

    def readByte(self, PtrOffset):
        ''' return the value read '''
        print >> sys.stderr, "read area 0x%x"%(PtrOffset, )
        self.bus.write_byte( self.i2cAddr, PtrOffset )
        val = self.bus.read_byte( self.i2cAddr )
        print >>sys.stderr, "Read value 0x%x"%val
        return val

 
 # the program starts from here
if __name__ == "__main__":
    # example
    
#     # write random byte to register on an EEPROM chip
#     eeprom = i2cDevice( BusToUse = 1, i2cAddr = 0x20) 
#     w_val = eeprom.writeRandom(0x00)
#     time.sleep(0.1)
#     r_val = eeprom.readByte(0x00)
#     
#     if w_val == r_val:
#        print "Read value corresponds to the written value: 0x%x"%w_val
#     else:
#        print "Read/write mismatch: 0x%x vs 0x%x"%(r_val, w_val)


    # make an LED blink on an MCP23017
    # Alternating high and low output on GPIOA0
    
    # Init i2c device class
    mcp = i2cDevice( BusToUse = 1, i2cAddr = 0x20 ) # using defaults
 
    
    mcp.writeByte( 0x00, 0x00 ) # set bank A to output on all pins
    portAddr = 0x14     # GPIO A0

    # and start blinking
    while True:
        print "Light on"
        mcp.writeByte( portAddr, 0x01 )
        time.sleep( 1.0 )
        print "Light off"
        mcp.writeByte( portAddr, 0x00 )
        time.sleep( 1.0 )


