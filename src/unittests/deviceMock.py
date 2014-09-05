'''
Created on Sep 5, 2014

@author: moz
'''

class deviceMock(object):
    '''
    classdocs
    '''


    def __init__(self, name):
        '''
        Constructor
        '''
        self._name = name
        self._setRetVal = True
        self._getRetVal = 0x23
        
    def getName(self):
        return self._name

    # get/set of write functionality    
    def setReturnOnSet(self, val):
        self._setRetVal = val
    
    def setAddress(self, addr, val ):
        return self._setRetVal
    
    # get/set of read functionality    
    def setReturnOnGet(self, val):
        self._getRetVal = val
    
    def getAddress(self, addr ):
        return self._getRetVal
    
    