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

# Start the robocall_server
        $ python ./robocall_server.py


# Making a call request from any web client
        http://192.168.25.220:8080/robocall?roomId=6001


# Reference
* https://www.lessons4you.info/how-to-originate-call-from-asterisk-cli/
* https://www.voip-info.org/wiki/view/Asterisk+cmd+Originate+Chinese

(譯者註:originate的用途是向客戶端發起呼叫，將客戶端引入到Dialplan中，並從exten的首項開始執行，進行一系列操作。雖然客戶端是被動接受，但此過程相當於主動撥入的過程。CLI> channel originate DAHDI/1/0123456789 extension 123@from-pstn  會從 DAHDI/1 界面撥號0123456789, 相當於外面有人播入到 dialplan 123)
* https://www.voip-info.org/wiki/view/Asterisk+auto-dial+out
