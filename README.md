# robocall
Robocall is a web service to make a phone call to deliver a pre-recorded messages from AMR robot. 
Also, the call will deliver a password code (defined by the "pw" parameter in the request URI)
Callee must anwser the call and press a "0" to confirm, or the caller will redial for several times.

# Hardware
#### Digium, Inc. Wildcard A4B 4-port analog card (PCI-Express) (rev 01)
1) Device Installation: please follow Ch.4 in the [user manual](https://www.digium.com/sites/digium/files/analog-telephony-card-4-port-user-manual.pdf).

    > No need to plug 12V power socket.

2) Check the Installation Correctly.

        # In Terminal, check the device.
        lspci -n
        # It show show a device with vendor ID = d161.

## Dependancy
Please follow the procedure to install asterisk server & dahdi driver.

1) Install asterisk

    Asterisk is a software implementation of a telephone private branch exchange (PBX). It allows telephones interfaced
    with a variety of hardware technologies to make calls to one another, and to connect to telephony services,
    such as the public switched telephone network (PSTN) and voice over Internet Protocol (VoIP) services.
    Its name comes from the asterisk symbol "*". - from [wiki](https://en.wikipedia.org/wiki/Asterisk_(PBX))

        sudo apt-get install asterisk

2) Install Dahdi (Digium/Asterisk Hardware Device Interface)

        wget https://downloads.asterisk.org/pub/telephony/dahdi-linux-complete/dahdi-linux-complete-current.tar.gz
        tar xzvf dahdi-linux-complete-current.tar.gz
        cd dahdi-linux-complete-X.XX.X+X.XX.X
        # USE ROOT
        sudo su
        make
        make install

 > ※ Check **/etc/init.d/dahdi** exist.
 >    if it doesn't exist, try :
 >  $ **sudo apt-get install asterisk-dahdi**

3) Load the Device Driver and Configuration

        # USE ROOT
        sudo su
        # load it as a kernel module to the Linux kernel
        modprobe wcaxx
        # Generate Dahdi configure file
        dahdi_genconf -vvvvv
        # Configure the channels
        dahdi_cfg -vvvvv

    # Check wcaxx is not blocked.
    > check wcaxx is not listed in **"/etc/modprobe.d/dahdi-blacklist.conf"**
    > If it's list, comment it out.


## robocall package

1. Install Dependency

        sudo pip install cherrypy

        # If you encounter installation error related to a module call SIX.
        # You can reinstall the SIX module
        # $ sudo -H pip install --ignore-installed six

2. Clone the package and replace the configuration files.

        git clone https://github.com/advancedroboticsaws/robocall.git
        cd ~/robocall
        sudo cp extensions.conf /etc/asterisk/extensions.conf
        sudo cp sip.conf /etc/asterisk/sip.conf
        sudo cp chan_dahdi.conf /etc/asterisk/chan_dahdi.conf
        sudo cp dahdi-channels.conf /etc/asterisk/dahdi-channels.conf

## Test the function.
1) Check the function Boost correctly

        # check the dahdi(wcaxx) driver is loaded
        lsmod | grep wcaxx
        # It shoould show sth like:
        >> dahdi                 225280  15 wcaxx,dahdi_transcode,oct612x"
        # Otherwise, Check wcaxx is not blocked.

        # Check the asterisk
        ps ax | grep asterisk


2) Use asterisk CLI to test basic calling.
    * Start the Asterisk CLI function
        $ asterisk -rvvvvvv
    * Use the command line in the CLI for dial a test call

        $ channel originate DAHDI/1/XX extension 100@from-internal
        > XX : set your internal phone extension number.

3) Test robocall.
   Run the robocall function.

        sudo python ./robocall_server.py

   Use brower to send the http request.

        http://192.168.30.222:8080/robocall?roomId=101&pw=0000

        // Please replace the IP address.
        // pw = password to prompt to the user
        // roomId = room id to call


### Add the robocall into startup script.
 Add following line into **/etc/rc.local**
 > /usr/bin/python /home/advrobot/robocall/robocall_server.py






### Configuration Note:
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




## Relative info

### Response
* Status: Completed  // 有接通 且有按 0
* Status: Expired    // 沒接通 或是沒按 0
* Status: Invalid roomId   // 無效的房號

### Convert wav file to gsm file
* wav file must be in 16 bit 8000 Hz stereo

        $ sox file1.wav -r 8000 -c 1 -s file1.gsm -q

* copy gsm files to /home/advrobot/robocall/sounds/

## Installation Reference
* https://www.lessons4you.info/how-to-originate-call-from-asterisk-cli/
* https://www.voip-info.org/wiki/view/Asterisk+cmd+Originate+Chinese

(譯者註:originate的用途是向客戶端發起呼叫，將客戶端引入到Dialplan中，並從exten的首項開始執行，進行一系列操作。雖然客戶端是被動接受，但此過程相當於主動撥入的過程。CLI> channel originate DAHDI/1/0123456789 extension 123@from-pstn  會從 DAHDI/1 界面撥號0123456789, 相當於外面有人播入到 dialplan 123)

* https://www.digium.com/sites/digium/files/analog-telephony-card-4-port-user-manual.pdf
* https://www.voip-info.org/wiki/view/Asterisk+auto-dial+out
* http://draalin.com/installing-asterisk-in-ubuntu/
* https://www.digium.com/sites/digium/files/digium-telephony-card-quickstart-installation-guide.pdf


