### requires multimon-ng
### https://github.com/EliasOenal/multimon-ng

#https://github.com/Schrolli91/BOSWatch/blob/master/boswatch.py





import logging
import logging.handlers
import subprocess


logpath = "/var/ramtmp"


# ##logging stuff
# #
# 	# Create new myLogger...
# 	#
# 	try:
# 		myLogger = logging.getLogger()
# 		myLogger.setLevel(logging.DEBUG)
# 		# set log string format
# 		#formatter = logging.Formatter('%(asctime)s - %(module)-15s %(funcName)-15s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')
# 		formatter = logging.Formatter('%(asctime)s - %(module)-15s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')
# 		# create a file logger
# 		# fh = MyTimedRotatingFileHandler.MyTimedRotatingFileHandler(globalVars.log_path+"boswatch.log", "midnight", interval=1, backupCount=999)
# 		# Starts with log level >= Debug
# 		# will be changed with config.ini-param later
# 		fh.setLevel(logging.DEBUG)
# 		fh.setFormatter(formatter)
# 		myLogger.addHandler(fh)
# 		# create a display logger
# 		ch = logging.StreamHandler()
# 		# log level for display: Default: info
# 		# if args.verbose:
# 		# 	ch.setLevel(logging.DEBUG)
# 		# elif args.quiet:
# 		# 	ch.setLevel(logging.CRITICAL)
# 		# else:
# 		# 	ch.setLevel(logging.INFO)
# 		ch.setFormatter(formatter)
# 		myLogger.addHandler(ch)

# 	except:
# 		# we couldn't work without logging -> exit
# 		print "ERROR: cannot create logger"
# 		exit(1)

    

#https://unix.stackexchange.com/questions/358138/directions-to-mixing-two-audio-streams
#https://askubuntu.com/questions/421014/share-an-audio-playback-stream-through-a-live-audio-video-conversation-like-sk



#outputs
#espeak "Hello world" --stdout | paplay -d 1
#pactl move-sink-input 15 Virtual2.monitor
#pactl move-source-output 2 Virtual1.monitor



#https://askubuntu.com/questions/421014/share-an-audio-playback-stream-through-a-live-audio-video-conversation-like-sk






##put multimon somewhere
multimon_ng = None


# test_source='sox -t wav /home/pi/sources/SIPERradio/dtmftones.wav -esigned-integer -b16 -r 22050 -t raw'
# test_source='paplay /home/pi/sources/SIPERradio/dtmftones.wav'
test_source='sox -t wav /home/pi/sources/SIPERradio/dtmftones.wav -esigned-integer -b16 -r 22050 -t raw pocsag_short.raw'



proc_src = subprocess.Popen(test_source.split(),
	stdout=subprocess.PIPE)

multimonconfig='multimon-ng -a DTMF -'

multimon_ng = subprocess.Popen(multimonconfig.split(),
        stdin=proc_src.stdout,
        stdout=subprocess.PIPE
    # stderr=open(globalVars.log_path+"multimon.log","a"),
        )



try:
    while True:
            nextline = multimon_ng.stdout.readline()
            multimon_ng.poll()
            print('line')
            sys.stdout.flush()

            if nextline.__contains__("DTMF:"):    # filter out only the alpha
                    nextline = nextline.split('DTMF: ')[1]
                    sys.stdout.write(timestamp() + " " + nextline)
                    sys.stdout.flush()
except:
        pass

multimon_ng.kill()



# Start multimon
#
# try:
#     # if not args.test:
#         # logging.debug("starting multimon-ng")
#         # command = ""
#         # if globalVars.config.has_option("BOSWatch","multimon_path"):
#         #     command = globalVars.config.get("BOSWatch","multimon_path")
#         # command = command+"multimon-ng "+str(demodulation)+" -f alpha -t raw /dev/stdin - "
#         #sox -t wav dtmftones.wav -esigned-integer -b16 -r 22050 -t raw - | multimon-ng -a DTMF -
        
#         command ="sox -t wav dtmftones.wav -esigned-integer -b16 -r 22050 -t raw - | multimon-ng -a DTMF -"
        
#         multimon_ng = subprocess.Popen(command.split(),
#             stdout=subprocess.PIPE,
#             # stderr=open(globalVars.log_path+"multimon.log","a"),
#             shell=False)
#         # multimon-ng  doesn't self-destruct, when an error occurs
#         # wait a moment to give the subprocess a chance to write the logfile
#         # time.sleep(3)
#         # checkSubprocesses.checkMultimon()
#     else:
#         logging.warning("!!! Test-Mode: multimon-ng not started !!!")
# except:
#     # we couldn't work without multimon-ng -> exit
#     logging.critical("cannot start multimon-ng")
#     logging.debug("cannot start multimon-ng", exc_info=True)
#     exit(1)
