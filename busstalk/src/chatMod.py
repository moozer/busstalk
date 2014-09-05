'''
Created on Sep 3, 2014

@author: moz
'''

import sys

class chatMod(object):
    '''
    classdocs
    '''

    def __init__(self, deviceList):
        '''
        Constructor
        '''
        self._cmdCount = 0
        if type( deviceList ) == type( [] ):
            self._devices = deviceList
        else:
            self._devices = [deviceList]            
        
    def _firstContact(self, command):
        expCmd = "GREETINGS"
        if command != "GREETINGS":
            print >> sys.stderr, "First contact failed: got '%s' expected '%s'"%(command, expCmd)
            retString = "ERROR got '%s' expected '%s'"%(command, expCmd)
            return False, retString
        
        retString = 'WELCOME'
        return True, retString
    
    def _sendUnknownCommand(self, command):
        ''' catch-all function to handle misspelling and the like '''
        print >> sys.stderr, "Unknown command:'%s'"%(command, )
        retString = "ERROR UNKOWN COMMAND '%s'"%(command, )
        return True, retString
    
    def _sendDevices(self, command):
        retString = "OK %s %s"%(command, ' '.join( d.getName() for d in self._devices ))
        return True, retString

    def _sendQuit(self, command):
        retString = "OK BYE"
        return False, retString
    
    def parse(self, command):
        ''' command is a oneline string without newline
        '''
        self._cmdCount += 1
        
        if self._cmdCount == 1: # first command
            return self._firstContact( command )
        
        if command == "DEVICES": # request device list
            return self._sendDevices( command )
        
        if command == "QUIT": # request device list
            return self._sendQuit( command )
        
        return self._sendUnknownCommand(command)
    