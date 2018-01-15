# robocall
Robocall is a web service to make a phone call to deliver a pre-recorded messages from AMR robot. 

# Dependancy
* Asterisk installation
Please follow the procedure to install asterisk server.

http://draalin.com/installing-asterisk-in-ubuntu/

* config /etc/asterisk/extensions.conf

        [from-internal]
        exten = 100,1,Answer()
        same = n,Wait(1)
        same = n,Playback(hello-world)
        same = n,Hangup()

* config /etc/asterisk/sip.conf

        [general]
        context=default
        
        [6001]
        type=friend
        context=from-internal
        host=dynamic
        secret=unsecurepassword
        disallow=all
        allow=ulaw

* TODO: config /etc/asterisk/DAHDI.conf

# Run
        $ python ./robocall_server.py


# Example URI
        http://192.168.25.220:8080/robocall?roomId=6001

