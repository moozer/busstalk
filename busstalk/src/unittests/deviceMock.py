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
        
    def getName(self):
        return self._name

    
    def setReturnOnSet(self, val):
        self._setRetVal = val
    
    def setAddress(self, addr, val ):
        return self._setRetVal
    
    