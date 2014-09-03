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

  ERROR UNKNOWN COMMAND '<command>'
  
  This means that the command issued was unknown.
  
  

Command reference:
------------------

## GREETINGS

  Reply example: WELCOME

  This must be the first command to send. Anything else will result in a closed connection.

## QUIT

  Reply example: OK BYE
  
  This disconnects from the server and the servers shuts down.
  
