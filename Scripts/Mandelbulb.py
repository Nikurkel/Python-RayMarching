import pygame
import random
import sys
import math
pygame.init()

SIZE = 900
ITERATIONS = 20
MaxMarchSteps = 100
MaxMarchDist = 20
SurfaceError = 0.001

planeSize = 1.5
nearPlanePos = (0.75, 0.75, 2) #normals are always z direction
eyePos = (1.5, 1.5, 4)

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
	if not length:
		return vector
	return [vector[0] / length, vector[1] / length, vector[2] / length]

def getDist(p): # Mandelbulb Signed Distance Function
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
		n += 1
		p = (ro[0] + dO * rd[0], ro[1] + dO * rd[1], ro[2] + dO * rd[2])
		dS = getDist(p)
		if (dS < SurfaceError):
			break
		dO += dS
		if dO > MaxMarchDist:
			break
	return (dO, n)

def renderMandelbulb():
	for y in range(SIZE):
		u = map(y, 0, SIZE, -planeSize/2, planeSize/2)
		for x in range(SIZE):
			v = map(x, 0, SIZE, -planeSize/2, planeSize/2)
			v_temp = ((nearPlanePos[0] + u) - eyePos[0], (nearPlanePos[1] + v) - eyePos[1], nearPlanePos[2] - eyePos[2])
			rd = normalize_vector(v_temp)
			d = rayMarch(eyePos, rd)
			if d[0] < MaxMarchDist:
				p = (eyePos[0] + rd[0] * d[0], eyePos[1] + rd[1] * d[0], eyePos[2] + rd[2] * d[0])
				brigthness = 255 - 255 * d[1] / MaxMarchSteps
				col = (colorLimits(brigthness * p[0]),colorLimits(brigthness * p[1]),colorLimits(brigthness * p[2]))
				pygame.draw.rect( window, col , (x,y,1,1))
		handleTime()

renderMandelbulb()
while True:
	handleTime()