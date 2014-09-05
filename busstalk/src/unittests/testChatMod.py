'''
Created on Sep 3, 2014

@author: moz
'''
import unittest
from chatMod import chatMod
from unittests.deviceMock import deviceMock

quitCmd = "QUIT"
quitResponse = (False, "OK BYE")
greetCmd = "GREETINGS"
greetResponse = (True, "WELCOME")
devicesCmd = "DEVICES"
deviceName = "EEPROM"
deviceResponse = (True, "OK DEVICES %s"%deviceName)    
devicesResponse = (True, "OK DEVICES %s MCP"%deviceName)    

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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConstruct']
    unittest.main()