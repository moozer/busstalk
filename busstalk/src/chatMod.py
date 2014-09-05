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
        paramsNeeded = 3
        if len(paramsToSet) < paramsNeeded:
            retString = "ERROR PARAMETERS MISSING GOT %d EXPECTED %d"%(len(paramsToSet), paramsNeeded)
            return True, retString
            
        deviceName, setAddr, setValue = paramsToSet[:3]

        d = self._getDevice( deviceName )
        if not d:
            retString = "ERROR BAD DEVICE '%s'"%deviceName
            return True, retString
        
        # auto convert to integer
        try:
            addr = int( setAddr, 0 )
            val = int( setValue, 0 )
        except ValueError, e:
            retString = "ERROR BAD HEX VALUE '%s'"%e.message.split('\'')[1]
            return True, retString            
                
        success = d.setAddress( addr, val )
        
        if success:
            retString = "OK %s ADDRESS 0x%x SET TO 0x%x"%(deviceName, addr, val )
        else:
            retString = "ERROR %s FAILED TO SET ADDRESS 0x%x TO 0x%x"%(deviceName, addr, val )
            
        return True, retString
    
    def _sendGet(self, paramsToSet):
        paramsNeeded = 2
        if len(paramsToSet) < paramsNeeded:
            retString = "ERROR PARAMETERS MISSING GOT %d EXPECTED %d"%(len(paramsToSet), paramsNeeded)
            return True, retString        
        
        deviceName, getAddr = paramsToSet[:2]

        d = self._getDevice( deviceName )
        if not d:
            retString = "ERROR BAD DEVICE '%s'"%deviceName
            return True, retString
        
        # auto convert to integer
        try:
            addr = int( getAddr, 0 )
        except ValueError, e:
            retString = "ERROR BAD HEX VALUE '%s'"%e.message.split('\'')[1]
            return True, retString
            
              
        # return None on error"  
        val = d.getAddress( addr )
        
        if val:
            retString = "OK %s ADDRESS 0x%x VALUE 0x%x"%(deviceName, addr, val )
        else:
            retString = "ERROR %s FAILED TO READ ADDRESS 0x%x"%(deviceName, addr )
            
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
                
        if cmdList[0] == "GET": # request device list
            return self._sendGet( cmdList[1:] )
        
        return self._sendUnknownCommand(cmdList[0])
    