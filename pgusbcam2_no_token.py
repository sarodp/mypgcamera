#!usr/bin/python3
# -*- coding: utf-8 -*-

# pygame.camera +streaming +imagesave +linenotifyIMG

import time,os
import pygame.camera
from pygame.locals import *
import linenotify as LNF


DEVICE = '/dev/video0'
Cwidth, Cheight = 320,240
SIZE = (Cwidth,Cheight)
FILEPATH = '/home/pi/scr/'

token_key = '<your access token>'

headers = str("Authorization: Bearer "+token_key)


def camstream():
	#--init
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
	running = True

	while running:
		#camera background
		screen = camera.get_image(screen)

		#rectangle
		xcolor =(255,255,0)
		xrect = pygame.Rect(0, Cheight-20, Cwidth, 20)
		pygame.draw.rect(screen, xcolor, xrect)
		
		display.blit(screen, (0,0))
		#text
		xcolor = (0,0,255) 
		f00 = pygame.font.Font(None,14)  
		f01 = pygame.font.Font("Garuda-Bold.ttf",12)  
		msg = "C101: ประตูหน้า   " + time.strftime(" %d-%m-%Y  %I:%M:%S %p")
		display.blit(f01.render(msg,True,xcolor),(10,Cheight-20))

		#flip
		pygame.display.flip()


		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_s:
				#save imagefile
				xfilename = FILEPATH + time.strftime("pic%Y-%m-%d--%H%M%S.jpg")
				pygame.image.save(display, xfilename)
				print(">>save image file: %s \n" % xfilename)

				#line_notify+image upload
				xrtn = LNF.line_notifyIMG("test usbcam",xfilename,headers)
				print ("LINE>> status code, error string , total time\n ", xrtn)

		clock.tick(FPS)

	#--exit
	camera.stop()
	pygame.quit()
	return

if __name__ == '__main__':
	camstream()
