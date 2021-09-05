from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame

from functions import *
from classes import *

'''
GAMESTATE indicates the current state of the game
0: menu
1: play
2: pause
3: gameover
4: credits
5: win
'''
GAMESTATE = 0

ship = Ship()
enemies = Enemies()
blocks = Blocks()


def keyboard(key, x, y):
    global ship, enemies, blocks, GAMESTATE

    # Move keys
    if (key == b'a' or key == b'A') and GAMESTATE == 1:
        ship.moveLeft()
    elif (key == b'd' or key == b'D') and GAMESTATE == 1:
        ship.moveRight()

    # Space key
    elif key == b' ':

        # start game at menu, pause or credits
        if (GAMESTATE == 0 or GAMESTATE == 2 or GAMESTATE == 4):
            GAMESTATE = 1
            return

        # restart game at game over or win
        if GAMESTATE == 3 or GAMESTATE == 5:
            ship = Ship()  # new ship
            enemies = Enemies()  # new enimies
            blocks = Blocks()  #new blocks
            GAMESTATE = 1
            return

        # Fire at play
        ship.fire()

    # State control keys
    elif (key == b'p' or key == b'P') and GAMESTATE == 1:
        GAMESTATE = 2
    elif key == b'c' or key == b'C':
        GAMESTATE = 4
    elif key == b"\x1b":  # Esc key
        exit()
    else:
        return

    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 1)

    global ship, enemies, blocks, GAMESTATE

    # Menu
    if GAMESTATE == 0:
        drawMenu()

    # Pause
    elif GAMESTATE == 2:
        drawPause()
        drawPlayerInfo(ship.score, ship.lives)
    elif GAMESTATE == 3:
        drawGameover()
        drawPlayerInfo(ship.score, ship.lives)
    elif GAMESTATE == 4:
        drawCredits()
    elif GAMESTATE == 5:
        drawWin()
        drawPlayerInfo(ship.score, ship.lives)
    else:

        # Check for win
        if len(enemies.list) == 0:
            GAMESTATE = 5

            # play sound
            playSFX('win.wav')
            return

        # Check for gameover
        if ship.dead:
            GAMESTATE = 3
            return

        # Draw player score and lives
        drawPlayerInfo(ship.score, ship.lives)
        # Draw ship
        ship.draw()
        # Draw enimies
        enemies.draw()
        # Draw blocks
        blocks.draw()
        # Trace bullets
        Bullets.trace(ship, enemies, blocks)

    drawControls()

    glFlush()
    glutSwapBuffers()


def main():
    pygame.mixer.init()
    playSFX('start.wav')

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(1024, 1024)
    glutInitWindowPosition(250, 0)
    glutCreateWindow('Space Invaders')
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutKeyboardFunc(keyboard)

    glutMainLoop()


if __name__ == '__main__':
    main()
