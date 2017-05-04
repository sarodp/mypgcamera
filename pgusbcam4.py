#!usr/bin/python3
# -*- coding: utf-8 -*-
# pygame.camera +streaming +imagefile save
import sys,time, pygame.camera
from pygame.locals import *

DEVICE = ['/dev/video0',
		 '/dev/video1',
		 '/dev/video2',
		 '/dev/video3']	
Cwidth,Cheight = 320,240
SIZE0 = (Cwidth*2,Cheight*2)
SIZECAM = (Cwidth,Cheight)
FILEPATH = '/home/pi/scr/'
xcolor = [(255,255,0),(0,0,255)]
CAMPOS = [(Cwidth*0,Cheight*0),
          (Cwidth*1,Cheight*0),
          (Cwidth*0,Cheight*1),
          (Cwidth*1,Cheight*1)]

def camstream():
	pygame.init()
	pygame.display.set_caption("ทดสอบ USB Webcam x 4 ")
	display = pygame.display.set_mode(SIZE0, 0)

	f00 = pygame.font.Font(None,14)  
	f01 = pygame.font.Font("Garuda-Bold.ttf",12)  

	pygame.camera.init()
	cam0 = pygame.camera.Camera(DEVICE[0], SIZECAM)
	cam0.start()

	FPS = 100   #--frame per sec
	clock = pygame.time.Clock()
	running = True
	while running:
		scr0 = cam0.get_image()
		scr1 = cam0.get_image()
		scr2 = cam0.get_image()
		scr3 = cam0.get_image()

		xrect = pygame.Rect(0,Cheight-20, Cwidth, 20)
		pygame.draw.rect(scr0, xcolor[0], xrect)
		pygame.draw.rect(scr1, xcolor[0], xrect)
		pygame.draw.rect(scr2, xcolor[0], xrect)
		pygame.draw.rect(scr3, xcolor[0], xrect)

		msg0 = "C101: ถนน         " + time.strftime(" %d-%m-%Y  %I:%M:%S %p")
		msg1 = "C102: ประตูหน้า  " + time.strftime(" %d-%m-%Y  %I:%M:%S %p")
		msg2 = "C103: ประตูหลัง   " + time.strftime(" %d-%m-%Y  %I:%M:%S %p")
		msg3 = "C104: ห้องผจก. " + time.strftime(" %d-%m-%Y  %I:%M:%S %p")
		scr0.blit(f01.render(msg0,True,xcolor[1]),(10,Cheight-20))
		scr1.blit(f01.render(msg1,True,xcolor[1]),(10,Cheight-20))
		scr2.blit(f01.render(msg2,True,xcolor[1]),(10,Cheight-20))
		scr3.blit(f01.render(msg3,True,xcolor[1]),(10,Cheight-20))

		display.blit(scr0, CAMPOS[0])
		display.blit(scr1, CAMPOS[1])
		display.blit(scr2, CAMPOS[2])
		display.blit(scr3, CAMPOS[3])
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_s:
				xfilename = FILEPATH + time.strftime("pic%Y-%m-%d--%H%M%S.jpg")
				pygame.image.save(display, xfilename)
				print(">>save image file: %s " % xfilename)

		clock.tick(FPS)

	cam0.stop()
	pygame.quit()
	sys.exit(0)
	return

if __name__ == '__main__':
	camstream()
