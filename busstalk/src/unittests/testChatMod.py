'''
Created on Sep 3, 2014

@author: moz
'''
import unittest
from chatMod import chatMod
from unittests.deviceMock import deviceMock
from random import randint

quitCmd = "QUIT"
quitResponse = (False, "OK BYE")
greetCmd = "GREETINGS"
greetResponse = (True, "WELCOME")
devicesCmd = "DEVICES"
deviceName = "EEPROM"

setValue = randint( 0x00, 0xff ) # random value
setAddr = randint( 0x00, 0xff ) # random value
deviceResponse = (True, "OK DEVICES %s"%deviceName)    
devicesResponse = (True, "OK DEVICES %s MCP"%deviceName)    
deviceSetCommand = "SET %s 0x%x 0x%x"%(deviceName, setAddr, setValue)
deviceSetResponse = "OK %s ADDRESS 0x%x SET TO 0x%x"%(deviceName, setAddr, setValue)

getValue = randint( 0x00, 0xff ) # random value
getAddr = randint( 0x00, 0xff ) # random value
deviceGetCommand = "GET %s 0x%x"%(deviceName, getAddr)
deviceGetResponse = "OK %s ADDRESS 0x%x VALUE 0x%x"%(deviceName, getAddr, getValue)

class Test(unittest.TestCase):

    def testConstruct(self):
        c = chatMod( deviceMock("EEPROM") )
        
    def testParseQuit(self):
        c = chatMod( deviceMock("EEPROM") )
        
        ret = c.parse( greetCmd )
        self.assertEqual( ret, greetResponse )
        ret = c.parse( quitCmd )
        self.assertEqual( ret, quitResponse )

    def testParseDevice(self):
        c = chatMod( deviceMock(deviceName) )
        
        ret = c.parse( greetCmd )
        self.assertEqual( ret, greetResponse )
        ret = c.parse( devicesCmd )
        self.assertEqual( ret, deviceResponse )

    def testParseDevices(self):
        c = chatMod( [deviceMock(deviceName), deviceMock("MCP")] )
        
        ret = c.parse( greetCmd )
        self.assertEqual( ret, greetResponse )
        ret = c.parse( devicesCmd )
        self.assertEqual( ret, devicesResponse )

    def testParseSet(self):
        m = deviceMock(deviceName)
        c = chatMod( m )
        
        ret = c.parse( greetCmd )
        self.assertEqual( ret, greetResponse )

        m.setReturnOnSet( True )
        ret = c.parse( deviceSetCommand )
        self.assertEqual( ret, (True, deviceSetResponse) )

    def testParseGet(self):
        m = deviceMock(deviceName)
        c = chatMod( m )
        
        ret = c.parse( greetCmd )
        self.assertEqual( ret, greetResponse )

        m.setReturnOnGet( getValue )
        ret = c.parse( deviceGetCommand )
        self.assertEqual( ret, (True, deviceGetResponse) )

    def testParseSetBadDevice(self):
        m = deviceMock(deviceName+'XX')
        c = chatMod( m )
        
        ret = c.parse( greetCmd )
        self.assertEqual( ret, greetResponse )

        m.setReturnOnSet( True )
        ret = c.parse( deviceSetCommand )
        self.assertEqual( ret, (True, "ERROR BAD DEVICE 'EEPROM'") )

    def testParseGetBadDevice(self):
        m = deviceMock(deviceName+'XX')
        c = chatMod( m )
         
        ret = c.parse( greetCmd )
        self.assertEqual( ret, greetResponse )
 
        m.setReturnOnGet( getValue )
        ret = c.parse( deviceGetCommand )
        self.assertEqual( ret, (True, "ERROR BAD DEVICE 'EEPROM'") )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConstruct']
    unittest.main()