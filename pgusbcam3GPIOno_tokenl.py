#!usr/bin/python3
# -*- coding: utf-8 -*-
#
# pygame.camera +streaming +imagesave +linenotifyIMG+GPIO input
#
# author: sarodp@yahoo.com
# date: 1-may-2017
#-----------------------------------------------------------------

# wiring diagram from Raspberry Pi GPIO port 
# to pushbuttons swA, swB and swC.
#
#     GPIO-23 [pin16]------[swA]----| 
#     GPIO-24 [pin18]------[swB]----| 
#                                   |
#     GROUND  [pin20]---------------|
#                                   |
#     GPIO-25 [pin22]------[swC]----| 
#

import time,os,sys
import pygame.camera
from pygame.locals import *
import linenotify as LNF
import RPi.GPIO as GPIO

#00--init LINE Notify
TOKEN_KEY = '<your access_token>'
HEADERS = str("Authorization: Bearer "+TOKEN_KEY)
FLAG_LNF = False

#01--init camera
DEVICE = '/dev/video0'
CWIDTH, CHEIGHT = 320,240
SIZE = (CWIDTH,CHEIGHT)
FILEPATH = '/home/pi/scr/'


#02--GPIO, interrupt/callback
switch_used = False

#save image
def switchA(channel):
	global switch_used
	switch_used = True

#save image+LINE Notify
def switchB(channel):
	global switch_used
	global FLAG_LNF
	switch_used = True
	FLAG_LNF = True

#save image
def switchC(channel):
	global switch_used
	switch_used = True

def camstream():
	#0a--init GPIO
	global switch_used
	global FLAG_LNF
	swA = 16
	swB = 18
	swC = 22

	# debounce time in msec.
	msecdebounce = 300  

	# configure as board
	GPIO.setmode(GPIO.BOARD)                                 

	# pull up active, we can use ground closure
	GPIO.setup(swA, GPIO.IN, pull_up_down=GPIO.PUD_UP)        
	GPIO.setup(swB, GPIO.IN, pull_up_down=GPIO.PUD_UP)        
	GPIO.setup(swC, GPIO.IN, pull_up_down=GPIO.PUD_UP)        

	# interrupt & callback
	GPIO.add_event_detect(swA, GPIO.FALLING, callback=switchA, bouncetime=msecdebounce)
	GPIO.add_event_detect(swB, GPIO.FALLING, callback=switchB, bouncetime=msecdebounce) 
	GPIO.add_event_detect(swC, GPIO.FALLING, callback=switchC, bouncetime=msecdebounce) 

	#0b--init pygame
	pygame.init()
	display = pygame.display.set_mode(SIZE, 0)
	pygame.display.set_caption("ทดสอบ USB Webcam")
	
	pygame.camera.init()
	camera = pygame.camera.Camera(DEVICE, SIZE)
	camera.start()
	screen = pygame.surface.Surface(SIZE, 0, display)

	#--loop
	FPS = 25   #--frame per sec
	clock = pygame.time.Clock()
	switch_used = False
	running = True

	while running:
		#1=screen update
		#1aa--camera background
		screen = camera.get_image(screen)

		#1a--caption box
		xcolor =(255,255,0)
		xrect = pygame.Rect(0, CHEIGHT-20, CWIDTH, 20)
		pygame.draw.rect(screen, xcolor, xrect)

		display.blit(screen, (0,0))
		#1b--caption text
		xcolor = (0,0,255) 
		f00 = pygame.font.Font(None,14)  
		f01 = pygame.font.Font("Garuda-Bold.ttf",12)  
		msg = "C101: ประตูหน้า   " + time.strftime(" %d-%m-%Y  %I:%M:%S %p")
		display.blit(f01.render(msg,True,xcolor),(10,CHEIGHT-20))

		#1z--flip
		pygame.display.flip()
		pygame.display.update()

		#2=do switchA,B,C
		if switch_used == True:
			#save imagefile
			xfilename = FILEPATH + time.strftime("pic%Y-%m-%d--%H%M%S.jpg")
			pygame.image.save(display, xfilename)
			print(">>save image file: %s \n" % xfilename)
			switch_used = False
			if FLAG_LNF:
				xrtn = LNF.line_notifyIMG("test usbcam",xfilename,HEADERS)
				print ("LINE>> status code, error string , total time\n ", xrtn)
				FLAG_LNF = False

		#3=pygame.event...
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_q:
				running = False
			elif event.type == KEYDOWN and event.key == K_s:
				#save imagefile
				xfilename = FILEPATH + time.strftime("pic%Y-%m-%d--%H%M%S.jpg")
				pygame.image.save(display, xfilename)
				print(">>save image file: %s \n" % xfilename)

				#line_notify+image upload
				if FLAG_LNF:
					xrtn = LNF.line_notifyIMG("test usbcam",xfilename,HEADERS)
					print ("LINE>> status code, error string , total time\n ", xrtn)

		#9=clock.tick
		clock.tick(FPS)

	#--exit
	camera.stop()
	pygame.quit()
	GPIO.cleanup()
	print ('\n system.exit(0)')
	sys.exit(0)         

	return

if __name__ == '__main__':
	camstream()
