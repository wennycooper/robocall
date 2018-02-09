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
    def robocall(self, roomId=0, pw=1234):
        roomIdSet = set([
            '11','12','15','0100','0015',
            '0201','0202','0203','0204','0205','0206','0207','0208','0209','0210','0211','0212','0213','0214','0215','0216','0217','0218','0219','0220','0221','0222',
            '0301','0302','0303','0304','0305','0306','0307','0308','0309','0310','0311','0312','0313','0314','0315','0316','0317','0318','0319','0320','0321','0322',
            '0401','0402','0403','0404','0405','0406','0407','0408','0409','0410','0411','0412','0413','0414','0415','0416','0417','0418','0419','0420','0421','0422',
            '0501','0502','0503','0504','0505','0506','0507','0508','0509','0510','0511','0512','0513','0514','0515','0516','0517','0518','0519','0520','0521','0522',
            '0601','0602','0603','0604','0605','0606','0607','0608','0609','0610','0611','0612','0613','0614','0615','0616','0617','0618','0619','0620','0621','0622',
            '0701','0702','0703','0704','0705','0706','0707','0708','0709','0710','0711','0712','0713','0714','0715','0716','0717','0718','0719','0720','0721','0722',
            '0801','0802','0803','0804','0805','0806','0807','0808','0809','0810','0811','0812','0813','0814','0815','0816','0817','0818','0819','0820','0821','0822'
            ])

        if str(roomId) not in roomIdSet:
            return "Status: Invalid roomId"

        user_pick_up = False
        loop_count = 0
        
        while loop_count<3:
            if not user_pick_up:
                p = subprocess.Popen('asterisk -rvvvvv',shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                p.stdin.write('dialplan set global pw '+pw+'\n')
                ss0 = 'channel originate DAHDI/1/'+str(int(roomId))+' extension 100@from-internal\n'
                print ss0
                p.stdin.write(ss0)
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
