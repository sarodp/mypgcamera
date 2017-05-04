#!usr/bin/python3
# -*- coding: utf-8 -*-
# pygame.camera +streaming +imagefile save
import sys,time, pygame.camera
from pygame.locals import *

DEVICE0 = '/dev/video0'
CAMW,CAMH = 320,240
SIZE0 = (CAMW,CAMH+20)
SIZECAM = (CAMW,CAMH)
FILEPATH = '/home/pi/scr/'
xcolor =[(255,255,0),(0,0,255)]

def camstream():
	pygame.init()
	pygame.display.set_caption("ทดสอบ กล้องเว็บแคม USB")
	display = pygame.display.set_mode(SIZE0, 0)

	f01 = pygame.font.Font("Garuda-Bold.ttf",12)  

	pygame.camera.init()
	camera = pygame.camera.Camera(DEVICE0, SIZECAM)
	camera.start()
	surfcam = pygame.surface.Surface(SIZECAM)

	FPS = 25   
	clock = pygame.time.Clock()
	running = True
	while running:
		camera.get_image(surfcam)
		display.blit(surfcam, (0,0))

		xrect = pygame.Rect(0, CAMH, CAMW, 20)
		pygame.draw.rect(display, xcolor[0], xrect)
		msg = "กล้อง #1: ประตูหน้า   " + time.strftime(" %d-%m-%Y %I:%M:%S %p")
		display.blit(f01.render(msg,True,xcolor[1]),(10,CAMH))

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_s:
				xfilename = FILEPATH + time.strftime("pic%Y-%m-%d__%H%M%S.jpg")
				pygame.image.save(display, xfilename)
				print(">>save image file: %s " % xfilename)

		clock.tick(FPS)

	camera.stop()
	pygame.quit()
	sys.exit(0)
	return

if __name__ == '__main__':
	camstream()
