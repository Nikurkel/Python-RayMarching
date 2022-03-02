import pygame
import random
import sys
import math
pygame.init()

SIZE = 800
ITERATIONS = 20
SHOW_AXIS = True
speed = 0 # 0 -> as fast as possible, n -> n/second
window = pygame.display.set_mode((SIZE,SIZE))
clock = pygame.time.Clock()

def windowMap(value, min, max):
	return min + ((value / SIZE) * (max - min))

def handleTime():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	clock.tick(speed)
	pygame.display.update()

def renderMandelbrot():
	for y in range(SIZE):
		for x in range(SIZE):
			c = (windowMap(x, -2.1, 2.1), windowMap(y, -2.1, 2.1)) # defining rendered area (xMinMax, yMinMax)
			z = (0,0)
			for i in range(ITERATIONS):
				if SHOW_AXIS and (c[0] == 0 or c[1] == 0):
					pygame.draw.rect( window, (255,0,0), (x,y,1,1))
					break
				z = (z[0]**2 - z[1]**2 + c[0], 2 * z[0] * z[1] + c[1])
				if math.dist((0,0), z) > 2:
					col = i * 255 / ITERATIONS
					pygame.draw.rect( window, (col,col,col), (x,y,1,1))
					break
				
		handleTime()

renderMandelbrot()

while True:
	handleTime()