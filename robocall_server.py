#!/usr/bin/python
#from __future__ import print_function
import cherrypy
import requests
import os
import os.path
import sys,time,subprocess,re
from subprocess import Popen, PIPE, STDOUT
from pushy import PushyAPI

class robocall_server(object):
    push_token=[]

    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def set_token(self,token):
        if not token in self.push_token:
            self.push_token.append(token)
        print(self.push_token)
        return "set token:"+token

    @cherrypy.expose
    def push(self,msg):
        print ('push:'+msg)
        data = {'message': msg}
        PushyAPI.sendPushNotification(data, self.push_token, None)
        return "notification pushed:"+msg
    
    @cherrypy.expose
    def shutdown(self):  
        cherrypy.engine.exit()


    @cherrypy.expose
    def robocall(self, roomId=0, pw=1234):
        roomIdSet = set([
            '100',
            '201','202','203','204','205','206','207','208','209','210','211','212','213',
            '301','302','303','304','305','306','307','308','309','310','311','312','313','314','315','316','317','318','319','320','321','322',
            '401','402','403','404','405','406','407','408','409','410','411','412','413','414','415','416','417','418','419','420','421','422',
            '501','502','503','504','505','506','507','508','509','510','511','512','513','514','515','516','517','518','519','520','521','522',
            '601','602','603','604','605','606','607','608','609','610','611','612','613','614','615','616','617','618','619','620','621','622',
            '701','702','703','704','705','706','707','708','709','710','711','712','713','714','715','716','717','718','719','720','721','722',
            '801','802','803','804','805','806','807','808','809','810','811','812','813','814','815','816','817','818','819','820','821','822'
            ])

        if str(roomId) not in roomIdSet:
            return "Status: Invalid roomId"

        user_pick_up = False
        loop_count = 0
        
        while loop_count<3:
            if not user_pick_up:
                p = subprocess.Popen('asterisk -rvvvvv',shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                p.stdin.write('dialplan set global pw '+pw+'\n')
                ss0 = 'channel originate DAHDI/1/6'+str(int(roomId))+' extension 100@from-internal\n'
                print(ss0)
                p.stdin.write(ss0)
                while True:
                    line = p.stdout.readline()
                    if re.search("Hungup",line) is None:
                        print(line.rstrip())
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
           print("request push notification!")
           # push notification
           msg = "robocall no answer to room: "+str(roomId) 
           s00 = requests.Session()
           r00 = s00.get('http://192.168.65.100:8080/' + 'push?msg=' + msg)
           return "Status: Expired"

        return str(value)
        #return "robocall with roomId = " + str(int(roomId))

if __name__ == '__main__':
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.thread_pool = 10
    cherrypy.quickstart(robocall_server())
