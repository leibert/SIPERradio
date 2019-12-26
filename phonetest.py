######################


#use espeak
##mixer for both espeak and audo
###https://raspberrypi.stackexchange.com/questions/92196/how-can-i-direct-the-output-both-of-mpg123-and-of-espeak-to-the-same-alsa-sound


import time
import sys
import subprocess
import os

from datetime import timedelta
from select import select
import re
from threading import Thread
import queue



# https://github.com/ccreutzig/rotopi/blob/master/linphone.py


class Linphone(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        subprocess.call(['killall', '-9', 'linphonec'])
        self.pipe = subprocess.Popen("/home/pi/linphone-desktop/OUTPUT/no-ui/bin/linphonec",
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.queue = queue
        self.daemon = True

    def sendDTMF(self, number):
        self.pipe.stdin.write(number)
        self.pipe.stdin.write("\n")

    def answer(self):
        self.pipe.stdin.write("answer\n")

    def hangup(self):
        self.pipe.stdin.write("terminate\n")

    def call(self, number):
        self.pipe.stdin.write("call sip:%s@voip.linode.org\n" % number)

    def run(self):
        while 1:
            status = select([self.pipe.stdout, self.pipe.stderr], [],
                [self.pipe.stdout, self.pipe.stderr])
            if status[2] != []:
                # error condition, better restart linphonec
                self.pipe.close
                self.pipe = subprocess.Popen("linphonec",
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            line = status[0][0].readline().decode('utf-8')
            print(line)
            m = re.search('Receiving new incoming call from (.*),', line)
            if m:
                self.queue.put(['incoming', m.group(1)])
            m = re.search('Call .* with (.*) ended', line)
            if m:
                self.queue.put(['disconnected', m.group(1)])
            m = re.search('Call .* with (.*) connected.', line)
            if m:
                self.queue.put(['connected', m.group(1)])
            m = re.search('User is busy.', line)
            if m:
                self.queue.put(['busy'])
            m = re.search('Call .* with (.*) error\\.', line)
            if m:
                self.queue.put(['error', m.group(1)])








def processDTMFCommand(commandString):
    print ("processing command")
    print(commandString)

    return True


# linphonec=subprocess.Popen("/home/pi/linphone-desktop/OUTPUT/no-ui/bin/linphonec",
#     stdin=subprocess.PIPE,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     universal_newlines=True) #this is for text communication
# #linphonec.stdin.write("proxy list\n")


# # multimon_ng = subprocess.Popen("sudo rtl_fm -f 173.240M -M fm -s 22050 -p 37 -E dc -F 0 -g 40 | multimon-ng -a POCSAG1200 -f alpha -t raw -",
# multimon_ng = subprocess.Popen("sox -t wav /home/pi/sources/SIPERradio/dtmftones.wav -esigned-integer -b16 -r 22050 -t raw - | multimon-ng -a DTMF -",
#     stdout=subprocess.PIPE,
#     shell=True)

#how long radio user has to enter a valid dtmf code
dialTimeout=30

#hold last time
timeoutClock=time.time()
dialString=""





eventQueue = queue.Queue()
linphone = Linphone(eventQueue)
linphone.start()



try:






    while (True):
        # print("LINEPHONE OUTPUT")
        # linphoneOutput=linphonec.stdout.readline()
        # print(linphoneOutput)

        if eventQueue:
            print("item in queue")
            event=eventQueue.get()
            print(event)
        

except KeyboardInterrupt:
    os.kill(multimon_ng.pid, 9)