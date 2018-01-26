#!/usr/bin/python
import os.path
import time
import os

fname = "/var/spool/asterisk/outgoing_done/demo-congrats.call"
callLog = "/var/spool/asterisk/outgoing_done/demo-congrats.call"


def read_call_status(filename) :
    with open(fname) as fp:
         for line in fp:
             strList = line.split(": ")
             if strList[0] == "Status":       
	        if strList[1] == "Completed\n":
                   return 1 
                elif strList[1] == "Expired\n": 
                   return -1

FileExit = False
value = -1
while FileExit != True :
  FileExit = os.path.isfile(fname)
  if FileExit == True: 
     value = read_call_status(fname)
     break 
  time.sleep(1)
#print "check: value =",value
cmd = "rm "+callLog
os.system(cmd)
os._exit(value)




