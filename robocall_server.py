#!/usr/bin/python
import cherrypy
import os

class robocall_server(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def robocall(self, roomId=0):
        cmd = "echo kkuei | sudo -S asterisk -rx \"channel originate SIP/" + str(int(roomId)) + " extension 100@from-internal\""
        os.system(cmd)
        return "robocall with roomId = " + str((int(roomId)))

if __name__ == '__main__':
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.thread_pool = 10
    cherrypy.quickstart(robocall_server())
