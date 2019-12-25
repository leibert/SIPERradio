######################


#use espeak
##mixer for both espeak and audo
###https://raspberrypi.stackexchange.com/questions/92196/how-can-i-direct-the-output-both-of-mpg123-and-of-espeak-to-the-same-alsa-sound


import time
import sys
import subprocess
import os

from datetime import timedelta

# multimon_ng = subprocess.Popen("sudo rtl_fm -f 173.240M -M fm -s 22050 -p 37 -E dc -F 0 -g 40 | multimon-ng -a POCSAG1200 -f alpha -t raw -",
multimon_ng = subprocess.Popen("sox -t wav /home/pi/sources/SIPERradio/dtmftones.wav -esigned-integer -b16 -r 22050 -t raw - | multimon-ng -a DTMF -",
    stdout=subprocess.PIPE,
    shell=True)

#how long radio user has to enter a valid dtmf code
dialTimeout=30

#hold last time
timeoutClock=time.time()
dialString=""
try:
    while (True):
        line = multimon_ng.stdout.readline().decode("utf-8")
        
        if (time.time()-timeoutClock > dialTimeout):
            timeoutClock=time.time()
            dialString=""
            continue

        #multimon found a valid DTMF code
        if line.startswith('DTMF: '):
            #extract the DTMF tone
            DTMFvalue = line.split('DTMF: ')[1]
            print(f"DTMF ID FOUND{DTMFvalue}")
            #reset the timeout clock
            timeoutClock=time.time()

            #end of dial command
            if DTMFvalue == "#":
                processDTMFCommand(dialString)
                dialString=""
            
            #more than 6 tones have been entered
            elif len(dialString) > 6:
                processDTMFCommand(dialString)
                dialString=""

            #otherwise just append this tone to the running string
            else:
                dialString=dialString+DTMFvalue





        multimon_ng.poll()
        # print(line)
        

except KeyboardInterrupt:
    os.kill(multimon_ng.pid, 9)