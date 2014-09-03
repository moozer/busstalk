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

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testConstruct(self):
        c = chatMod()
        
    def testParseQuit(self):
        c = chatMod()
        
        ret = c.parse( greetCmd )
        self.assertEqual( ret, greetResponse )
        ret = c.parse( quitCmd )
        self.assertEqual( ret, quitResponse )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConstruct']
    unittest.main()