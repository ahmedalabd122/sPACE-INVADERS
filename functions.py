from math import sqrt
import pygame

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


'''
Helper Functions
'''
# Apply the grid scale on coordinats 
def scaled(num, scale = 15):
	return num/scale


# Handle floats precesion issue
def formated(num):
	return float("{:.2f}".format(num))


'''
Write text on the screen
'''
def renderText(text, position=(0,0), size=1, stroke=1, color=(1,1,1)):
	glPushMatrix()

	glColor3f(color[0], color[1], color[2]) # set color
	glLineWidth(stroke) # set letter stroke
	# translate to set position
	glTranslate(
		scaled(position[0]),
		scaled(position[1]),
		0
	)

	# scale to set size
	s = scaled(size / 1000)
	glScalef(s, s, s)

	for ch in text:
		glutStrokeCharacter( GLUT_STROKE_MONO_ROMAN, ctypes.c_int(ord(ch)) )
	glPopMatrix()


'''
Get distance between two points for collision
'''
def getDistance(pos1, pos2):
	x = pos1[0] - pos2[0]
	y = pos1[1] - pos2[1]

	return sqrt(x**2 + y**2)


'''
Draw functions
'''
def drawMenu():
	renderText('SPACE', (-4,1), 15, 6, (0,1,0))
	renderText('INVADERS', (-6.35,-1), 15, 6, (0,1,0))
	renderText('Press [space] to play', (-3,-2), 3, 2, (1,1,1))


def drawPlayerInfo(score, lives):
	glColor3f(1, 1, 1)
	glBegin(GL_LINES)
	glVertex3f(scaled(-10), scaled(10), 0)
	glVertex3f(scaled(10), scaled(10), 0)
	glEnd()

	renderText('Score:' + str(score), (-9.5,10.5), 3, 2, (1,1,1))
	renderText('Lives:' + str(lives), (7.5,10.5), 3, 2, (1,1,1))


def drawControls():
	glColor3f(1, 1, 1)
	glBegin(GL_LINES)
	glVertex3f(scaled(-10), scaled(-10), 0)
	glVertex3f(scaled(10), scaled(-10), 0)
	glEnd()

	renderText('[space] fire', (-9.5,-11), 3, 2, (1,1,1))
	renderText('[p] pause', (-4,-11), 3, 2, (1,1,1))
	renderText('[c] credits', (1,-11), 3, 2, (1,1,1))
	renderText('[esc] exit', (6.5,-11), 3, 2, (1,1,1))


def drawCredits():
	renderText('Made with love by', (-5.5,4), 6, 4, (0,1,0))
	renderText('Ahmed AlAbd', (-3.85,2.5), 6, 2, (1,1,1))
	renderText('Hamed Ali', (-3,1.25), 6, 2, (1,1,1))
	renderText('Mohamed Osama', (-4.25,0), 6, 2, (1,1,1))
	renderText('Abdulaziz Bargush', (-5.45,-1.25), 6, 2, (1,1,1))


def drawPause():
	renderText('PAUSED', (-2.5,0), 10, 4, (0,1,0))
	renderText('Press [space] to resume', (-3,-1), 3, 2, (1,1,1))


def drawGameover():
	renderText('GAMEOVER', (-3.5,0), 10, 4, (1,1,0))
	renderText('Press [space] to play again', (-3.5,-1), 3, 2, (1,1,1))


def drawWin():
	renderText('WINNER!', (-2.85,1.5), 10, 4, (1,0,1))
	renderText('WINNER!', (-2.85,0), 10, 4, (1,0,1))
	renderText('Press [space] to play again', (-3.5,-1), 3, 2, (1,1,1))


def playSFX(filename):
	pygame.mixer.music.load('sounds/' + filename)
	pygame.mixer.music.play()