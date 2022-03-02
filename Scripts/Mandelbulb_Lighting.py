import pygame
import random
import sys
import math
pygame.init()

SIZE = 800
ITERATIONS = 10
MaxMarchSteps = 100
MaxMarchDist = 100
SurfaceError = 0.003

planeSize = 1.5
nearPlane = (1.4, 2.5, 7) # normals are always z direction
eyePos = (2.5, 4, 10)
lightPos = (10, 15, 5)

framesPerSecond = 0
window = pygame.display.set_mode((SIZE,SIZE))
clock = pygame.time.Clock()

def handleTime():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	clock.tick(framesPerSecond)
	pygame.display.update()

def colorLimits(val):
	if val > 255:
		return 255
	if val < 0:
		return 0
	return val

def map(value, leftMin, leftMax, rightMin, rightMax):
	valueScaled = float(value - leftMin) / float(leftMax - leftMin)
	return rightMin + (valueScaled * (rightMax - rightMin))

def normalize_vector(vector):
	length = math.dist((0,0,0),vector)
	return (vector[0] / length, vector[1] / length, vector[2] / length)

def getDist(pos):
	m = mandelbulbDist(pos)
	r = min(pos[0] + 3, pos[1] + 3, pos[2] + 20)
	s = math.dist(lightPos, pos) - 0.3
	return min(m,r,s)

def mandelbulbDist(p):
	bailout = 2;
	Power = 8;
	z = p;
	dr = 1.0;
	r = 0.0;
	for _ in range(ITERATIONS):
		r = math.dist((0,0,0), z)
		if r > bailout:
			break 
		theta = math.acos(z[2] / r);
		phi = math.atan2(z[1], z[0]);
		dr = pow(r, Power - 1.0) * Power * dr + 1.0;
		zr = pow(r, Power);
		theta = theta * Power;
		phi = phi * Power;
		z = (zr * math.sin(theta) * math.cos(phi), zr * math.sin(phi) * math.sin(theta), zr * math.cos(theta))
		z = (z[0] + p[0], z[1] + p[1], z[2] + p[2])
	return 0.5 * math.log(r) * r / dr

def rayMarch(ro, rd):
	dO = 0
	dS = None
	n = 0
	for _ in range(MaxMarchSteps):
		n = n + 1
		p = (ro[0] + dO * rd[0], ro[1] + dO * rd[1], ro[2] + dO * rd[2])
		dS = getDist(p)
		dO += dS
		if dS < SurfaceError or dO > MaxMarchDist:
			break
	return (dO, n, dS)

def calcNormal(pos): 
    e = (0.01,0.0)
    n = normalize_vector((
    		(getDist(pos) - getDist((pos[0] + e[0], pos[1] + e[1], pos[2] + e[1]))),
    		(getDist(pos) - getDist((pos[0] + e[1], pos[1] + e[0], pos[2] + e[1]))),
    		(getDist(pos) - getDist((pos[0] + e[1], pos[1] + e[1], pos[2] + e[0])))))
    return n
    
def renderMandelbulb():
	for y in range(SIZE):
		v = map(y, 0, SIZE, planeSize/2, -planeSize/2)
		for x in range(SIZE):
			u = map(x, 0, SIZE, -planeSize/2, planeSize/2)
			v_temp = ((nearPlane[0] + u) - eyePos[0], (nearPlane[1] + v) - eyePos[1], nearPlane[2] - eyePos[2])
			rd = normalize_vector(v_temp)
			d = rayMarch(eyePos, rd)
			if d[0] < MaxMarchDist:
				p = (eyePos[0] + rd[0] * d[0] - rd[0] * d[2] * 10, eyePos[1] + rd[1] * d[0] - rd[1] * d[2] * 10, eyePos[2] + rd[2] * d[0] - rd[2] * d[2] * 10)
				# LIGHTING
				lightDir = normalize_vector((lightPos[0] - p[0], lightPos[1] - p[1], lightPos[2] - p[2]))
				dL = rayMarch(p, lightDir)
				c = colorLimits(20)
				if dL[0] > math.dist(p, lightPos) - 1:
					dif = math.dist(calcNormal(p), normalize_vector((-rd[0],-rd[1],-rd[2])))
					c = colorLimits(c + dL[1] * 10/dif)
					c = colorLimits(275 - c)
				pygame.draw.rect( window, (c,c,c), (x,y,1,1))
		handleTime()
	print("finished")

renderMandelbulb()
while True:
	handleTime()