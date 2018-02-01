# robocall
Robocall is a web service to make a phone call to deliver a pre-recorded messages from AMR robot. 
Callee must anwser the call and press 5 to confirm, or the caller will redial for 3 times.

# Dependancy
* Asterisk installation
Please follow the procedure to install asterisk server & dahdi driver.

http://draalin.com/installing-asterisk-in-ubuntu/
https://www.digium.com/sites/digium/files/digium-telephony-card-quickstart-installation-guide.pdf
https://www.digium.com/sites/digium/files/analog-telephony-card-4-port-user-manual.pdf

* config /etc/asterisk/extensions.conf

    [from-internal]
    exten = 100,1,Answer()
     same = n,Wait(1)
    ; same = n,NoOp(hello_kkuei)
    ; same = n,Playback(demo-instruct)
     same = n,Background(demo-instruct)
     same = n,WaitExten(30)
     same = n,Hangup()
    
    exten = 5,1,NoOp(KKUEI ext5)
    
    exten = 6,1,NoOp(KKUEI ext6)


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

* config /etc/dahdi/system.conf

    fxsks=1
    echocanceller=mg2,1
    fxsks=2
    echocanceller=mg2,2
    fxsks=3
    echocanceller=mg2,3
    fxsks=4
    echocanceller=mg2,4

    # Global data
    
    loadzone        = us
    defaultzone     = us

* config /etc/asterisk/chan_dahdi.conf

    ....
    [channels]
    #include /etc/asterisk/dahdi-channels.conf
    ....

* config /etc/asterisk/dahdi-channels.conf

    ;;; line="1 WCTDM/0/0 FXSKS  (EC: VPMOCT032 - INACTIVE)"
    signalling=fxs_ks
    callerid=asreceived
    group=0
    context=from-internal
    channel => 1
    callerid=
    group=
    context=default

# Start the robocall_server
        $ sudo python ./robocall_server.py


# Making a call request from any web client
        http://192.168.30.222:8080/robocall?roomId=15

# Response
* Status: Completed
* Status: Expired

# Reference
* https://www.lessons4you.info/how-to-originate-call-from-asterisk-cli/
* https://www.voip-info.org/wiki/view/Asterisk+cmd+Originate+Chinese

(譯者註:originate的用途是向客戶端發起呼叫，將客戶端引入到Dialplan中，並從exten的首項開始執行，進行一系列操作。雖然客戶端是被動接受，但此過程相當於主動撥入的過程。CLI> channel originate DAHDI/1/0123456789 extension 123@from-pstn  會從 DAHDI/1 界面撥號0123456789, 相當於外面有人播入到 dialplan 123)
* https://www.digium.com/sites/digium/files/analog-telephony-card-4-port-user-manual.pdf
* https://www.voip-info.org/wiki/view/Asterisk+auto-dial+out
