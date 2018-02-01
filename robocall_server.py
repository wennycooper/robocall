#!/usr/bin/python
import cherrypy
import os
import os.path
import sys,time,subprocess,re
from subprocess import Popen, PIPE, STDOUT

class robocall_server(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def robocall(self, roomId=0):
        user_pick_up = False
        loop_count = 0
        
        while loop_count<2:
            if not user_pick_up:
                p = subprocess.Popen('asterisk -rvvvvv',shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                p.stdin.write('channel originate DAHDI/1/'+roomId+' extension 100@from-internal\n')
                while True:
                    line = p.stdout.readline()
                    if re.search("Hungup",line) is None:
                        print line.rstrip()
                        if bool(re.search("NOTICE",line)):
                            print "Wait for dahdi channel resource!"
                            time.sleep(10)
                            break
                        elif bool(re.search("KKUEI ext0",line)):
                            user_pick_up = True
                    else:       # print "Hungup"
                        time.sleep(5)
                        if not user_pick_up:
                            print "Hangup but not pressing 0... back to loop"
                        loop_count += 1
                        break
            elif user_pick_up:
                print "user_picp_up == True"
                break
            else:
                pass


        if user_pick_up == True:
           return "Status: Completed"
        elif user_pick_up == False:
           return "Status: Expired"

        return str(value)
        #return "robocall with roomId = " + str(int(roomId))

if __name__ == '__main__':
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.thread_pool = 10
    cherrypy.quickstart(robocall_server())
