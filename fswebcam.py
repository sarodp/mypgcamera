import time,os

while True: # do forever
	# uses Fswebcam to take picture
	# $ man strftime //--man page string format time
	#os.system('fswebcam -r 320x240 -S 3 --jpeg 50 --save /home/pi/scr/fswebcam/pic%H%M%S.jpg') 
	os.system('fswebcam -r 320x240 -S 3 --jpeg 50 --save /home/pi/scr/fswebcam/pic%F%T.jpg') 

	# 15 second delay then loop
	time.sleep(1) 

