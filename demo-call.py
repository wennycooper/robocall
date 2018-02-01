#!/usr/bin/python
import sys,os

TEMPLATE_CALLFILE = "/home/advrobot/robocall/demo-congrats.call.TEMPLATE"
CALLFILE = "/home/advrobot/robocall/demo-congrats.call"
OUTGOING_PATH = "/var/spool/asterisk/outgoing/"
OUTGOING_DONE_PATH = "/var/spool/asterisk/outgoing_done/"

cmd1 = "cp " + TEMPLATE_CALLFILE + " " + CALLFILE
#cmd2 = "echo Channel: SIP/" + sys.argv[1] + " >> " + CALLFILE
cmd2 = "echo Channel: DAHDI/1/" + sys.argv[1] + " >> " + CALLFILE
cmd3 = "chmod 777 " + CALLFILE
cmd4 = "mv " + CALLFILE + " " + OUTGOING_PATH

os.system(cmd1)
os.system(cmd2)
os.system(cmd3)
os.system(cmd4)
