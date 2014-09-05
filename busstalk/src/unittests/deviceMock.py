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
        
    def getName(self):
        return self._name
    
    