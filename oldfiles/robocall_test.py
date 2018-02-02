#!/usr/bin/python
import sys,time,subprocess,re
from subprocess import Popen, PIPE, STDOUT
user_pick_up = False
loop_count = 0
while loop_count<3:
    if not user_pick_up:
        p = subprocess.Popen('sudo asterisk -rvvvvv',shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        p.stdin.write('channel originate DAHDI/1/15 extension 100@from-internal\n')
        while True:
            line = p.stdout.readline()
            if re.search("Hungup",line) is None:
                print line.rstrip()
                if bool(re.search("NOTICE",line)):
                    print "2000 YEARS LATER!"
                    time.sleep(10)
                    break
                elif bool(re.search("KKUEI ext5",line)):
                    user_pick_up = True
            else:       # print "Hungup"
                time.sleep(5)
                if not user_pick_up:
                    print "Answer ME!!!!!!!!!"
                loop_count += 1
                break
    elif user_pick_up:
        print "Finallllly!"
        break
    else:   
        pass