I2C on raspberry
================

There are some adjustments needed to enable i2c on the raspberry. It is described in the *Basic installation" link below.

To test the I2C, first use the i2cdetect

  i2cdetect -y 0
  i2cdetect -y 1

Some relevant links

* [Basic installation](http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/io-pins-raspbian/i2c-pins).
* [Python and I2C](http://www.raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2)


busstalk client/server
======================

The program is designed to give access to i2c on a raspberry over the LAN.

A specialized text-based protocol is used. This is suited for telnet access.


Installation:
-------------

To install the program it mus be fetched from github.

  sudo apt-get install git
  git clone https://github.com/moozer/busstalk.git


Using the program:
--------------------

On the raspberry pi, start the program using

  ./startScript.sh
  
On the client, start a terminal and run

  telnet <ip-address> 10000
  
to connect to the raspberry on tcp port 10000.


Command generalities:
--------------------

Whenever a command is issued there a two possible answers.

  OK <command> <more values>
  
  This means that the command was successful and data (if any) has been returned
  
or

  ERROR <some meaningful error message>
  
  This means that the command issued had an error. This could be bad hex values or other input issues
  
  

Command reference:
------------------

Yes, capital letters are mandatory

### GREETINGS

  Reply example: WELCOME

  This must be the first command to send. Anything else will result in a closed connection.

### QUIT

  Reply example: OK BYE
  
  This disconnects from the server and the servers shuts down.
  
### DEVICES

  Reply example: OK DEVICES MCF EEPROM
  
  The command queries the server and asks for the list of connected devices.
  
### SET <device> <addr> <value>

   Reply example: OK SET MCF ADDRESS 0x14 TO 0x01
   
   Send a data byte to the device and set the data at specified address
   
 
### GET <device> <addr>

   Reply example: OK GET MCF ADDRESS 0xf2 VALUE 0x00 
   
   Read from the device and return the value at the given address   
 

