'''
Created on Sep 3, 2014

@author: moz
'''
import unittest
from chatMod import chatMod

quitCmd = "QUIT"
quitResponse = (False, "OK BYE")
greetCmd = "GREETINGS"
greetResponse = (True, "WELCOME")
devicesCmd = "DEVICES"
devicesResponse = (True, "OK DEVICES EEPROM LED")

class Test(unittest.TestCase):

    def testConstruct(self):
        c = chatMod()
        
    def testParseQuit(self):
        c = chatMod()
        
        ret = c.parse( greetCmd )
        self.assertEqual( ret, greetResponse )
        ret = c.parse( quitCmd )
        self.assertEqual( ret, quitResponse )

    def testParseDevices(self):
        c = chatMod()
        
        ret = c.parse( greetCmd )
        self.assertEqual( ret, greetResponse )
        ret = c.parse( devicesCmd )
        self.assertEqual( ret, devicesResponse )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConstruct']
    unittest.main()