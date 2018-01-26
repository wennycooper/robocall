#!/usr/bin/python
import cherrypy
import os
import os.path
import time

class robocall_server(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def robocall(self, roomId=0):
        cmd = "/home/kkuei/catkin_ws/src/robocall/demo-call.py " + roomId
        cmd1 = "/home/kkuei/catkin_ws/src/robocall/check_call_status.py"
        os.system(cmd)
                
        value = os.system(cmd1)
        value = value >> 8
        print "call status = ", value
        if value == 1:
           return "Status: Completed"
        elif value == 255:
           return "Status: Expired"

        return str(value)
        #return "robocall with roomId = " + str(int(roomId))

if __name__ == '__main__':
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.thread_pool = 10
    cherrypy.quickstart(robocall_server())
