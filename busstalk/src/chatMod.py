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
    

    def _sendSet(self, paramsToSet):
        deviceName, setAddr, setValue = paramsToSet[:3]

        d = self._getDevice( deviceName )
        
        # auto convert to integer
        addr = int( setAddr, 0 )
        val = int( setValue, 0 )
                
        success = d.setAddress( addr, val )
        
        if success:
            retString = "OK %s address 0x%x set to 0x%x"%(deviceName, addr, val )
        else:
            retString = "ERROR %s failed to set address 0x%x to 0x%x"%(deviceName, addr, val )
            
        return True, retString
    
    def _getDevice(self, deviceName ):

        for d in self._devices:
            if deviceName == d.getName():
                return d
        
        return None
    
    def parse(self, command):
        ''' command is a oneline string without newline
        '''
        self._cmdCount += 1
        cmdList = command.split(' ')
        
        if self._cmdCount == 1: # first command
            return self._firstContact( cmdList[0] )
        
        if cmdList[0] == "DEVICES": # request device list
            return self._sendDevices( cmdList[0] )
        
        if cmdList[0] == "QUIT": # request device list
            return self._sendQuit( cmdList[0] )
        
        if cmdList[0] == "SET": # request device list
            return self._sendSet( cmdList[1:] )
                
        return self._sendUnknownCommand(cmdList[0])
    