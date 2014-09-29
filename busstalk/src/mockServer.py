
#!/usr/bin/python

'''
Created on Sep 5, 2014

This server is a simple moc, which can be used for testing the internet connection
without connecting to an I2C device

@author: moz
'''
from bsServer import bsServer

class device(object):
    '''
    classdocs
    '''
    def __init__(self):
        print "Mock device - not doing anything"

    def getName(self):
        return "MOCK"

    def setAddress(self, addr, val ):
        print "Writing"
        return True

    def getAddress(self, addr ):
        print "Reading"
        from random import randint
        SomeData = randint( 0, 0xff )
        return SomeData

if __name__ == '__main__':
    srv = bsServer( deviceList = device(), port = 10000)
    srv.start()



