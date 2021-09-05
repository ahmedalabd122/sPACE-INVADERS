import random, time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from functions import *


class Brick:
    def __init__(self):
        self.position = [0, 0]

    def draw(self):
        glBegin(GL_QUADS)

        glColor3f(0.2, 0.2, 0.5)
        glVertex(scaled(self.position[0] - 0.5), scaled(self.position[1] - 0.3), 0)
        glVertex(scaled(self.position[0] - 0.5), scaled(self.position[1] + 0.3), 0)
        glVertex(scaled(self.position[0] + 0.5), scaled(self.position[1] + 0.3), 0)
        glVertex(scaled(self.position[0] + 0.5), scaled(self.position[1] - 0.3), 0)

        glEnd()


class Blocks:
    def __init__(self):
        self.count = 9
        self.numOfBlocks = 3
        self.rows = 3
        self.position = [-8, -4]
        self.list = [Brick() for i in range(self.count)]

        self.generate()

    def generate(self):
        for u in range(self.numOfBlocks):
            for j in range(self.rows):
                self.list[j + u * self.rows].position = [
                    self.position[0] + j*7 + u * 1,
                    self.position[1]
                ]

    def draw(self):
        for brick in self.list:
            brick.draw()


class Ship:
    score = 0
    dead = False

    def __init__(self):
        self.posX = 0
        self.posY = scaled(-8)
        self.lives = 3
        self.takeDamage = {
            'state': False,
            'flashDuration': 0.15,  # in seconds
            'flashStart': None
        }

        # Reset score and dead
        Ship.score = 0
        Ship.dead = False

    def draw(self):

        if self.dead:
            self.lives = 0
            glColor3f(1, 0, 0)
        elif self.takeDamage['state']:
            if time.time() - self.takeDamage['flashStart'] > self.takeDamage['flashDuration']:
                self.takeDamage['state'] = False
            glColor3f(1, 0, 0)
        else:
            glColor3f(0, 1, 0)

        glBegin(GL_QUADS)
        # Bottom
        glVertex3d(self.posX + scaled(-.75), self.posY + scaled(-1), 0)
        glVertex3d(self.posX + scaled(-.75), self.posY + scaled(0), 0)
        glVertex3d(self.posX + scaled(.75), self.posY + scaled(0), 0)
        glVertex3d(self.posX + scaled(.75), self.posY + scaled(-1), 0)

        # Middle
        glVertex3d(self.posX + scaled(-0.65), self.posY + scaled(0), 0)
        glVertex3d(self.posX + scaled(-0.65), self.posY + scaled(0.15), 0)
        glVertex3d(self.posX + scaled(0.65), self.posY + scaled(0.15), 0)
        glVertex3d(self.posX + scaled(0.65), self.posY + scaled(0), 0)

        # Top
        glVertex3d(self.posX + scaled(-0.05), self.posY + scaled(0.15), 0)
        glVertex3d(self.posX + scaled(-0.05), self.posY + scaled(0.35), 0)
        glVertex3d(self.posX + scaled(0.05), self.posY + scaled(0.35), 0)
        glVertex3d(self.posX + scaled(0.05), self.posY + scaled(0.15), 0)
        glEnd()

    def moveRight(self):
        if self.posX >= scaled(9.25) or self.dead:
            return
        self.posX = formated(self.posX + scaled(.5))

    def moveLeft(self):
        if self.posX <= scaled(-9.25) or self.dead:
            return
        self.posX = formated(self.posX - scaled(.5))

    def fire(self):
        if self.dead: return

        altPos = [self.posX, self.posY + scaled(.75)]
        Bullets.add(altPos)

        # play sound
        playSFX('ship-laser.wav')

    def loseLive(self):
        self.lives -= 1
        self.takeDamage['state'] = True
        self.takeDamage['flashStart'] = time.time()

        if self.lives == 0:
            Ship.die()

    @staticmethod
    def increaseScore():
        Ship.score += 1

    @staticmethod
    def die():
        Ship.dead = True

        # play sound
        playSFX('gameover.wav')


class Enemy:

    def __init__(self):
        self.position = [0, 0]

    def draw(self):
        glBegin(GL_QUADS)

        glColor3f(1, 1, 1)
        glVertex(scaled(self.position[0] - 0.5), scaled(self.position[1] - 0.5), 0)
        glVertex(scaled(self.position[0] - 0.5), scaled(self.position[1] + 0.2), 0)
        glVertex(scaled(self.position[0] + 0.5), scaled(self.position[1] + 0.2), 0)
        glVertex(scaled(self.position[0] + 0.5), scaled(self.position[1] - 0.5), 0)

        glVertex(scaled(self.position[0] - 0.4), scaled(self.position[1] - 0.5), 0)
        glVertex(scaled(self.position[0] - 0.4), scaled(self.position[1] + 0.35), 0)
        glVertex(scaled(self.position[0] + 0.4), scaled(self.position[1] + 0.35), 0)
        glVertex(scaled(self.position[0] + 0.4), scaled(self.position[1] - 0.5), 0)

        glVertex(scaled(self.position[0] - 0.3), scaled(self.position[1] - 0.5), 0)
        glVertex(scaled(self.position[0] - 0.3), scaled(self.position[1] + 0.5), 0)
        glVertex(scaled(self.position[0] + 0.3), scaled(self.position[1] + 0.5), 0)
        glVertex(scaled(self.position[0] + 0.3), scaled(self.position[1] - 0.5), 0)

        glColor3f(0, 0, 0)
        glVertex(scaled(self.position[0] - 0.4), scaled(self.position[1] - 0.5), 0)
        glVertex(scaled(self.position[0] - 0.4), scaled(self.position[1] - 0.35), 0)
        glVertex(scaled(self.position[0] - 0.2), scaled(self.position[1] - 0.35), 0)
        glVertex(scaled(self.position[0] - 0.2), scaled(self.position[1] - 0.5), 0)

        glVertex(scaled(self.position[0] - 0.1), scaled(self.position[1] - 0.5), 0)
        glVertex(scaled(self.position[0] - 0.1), scaled(self.position[1] - 0.35), 0)
        glVertex(scaled(self.position[0] + 0.1), scaled(self.position[1] - 0.35), 0)
        glVertex(scaled(self.position[0] + 0.1), scaled(self.position[1] - 0.5), 0)

        glVertex(scaled(self.position[0] + 0.2), scaled(self.position[1] - 0.5), 0)
        glVertex(scaled(self.position[0] + 0.2), scaled(self.position[1] - 0.35), 0)
        glVertex(scaled(self.position[0] + 0.4), scaled(self.position[1] - 0.35), 0)
        glVertex(scaled(self.position[0] + 0.4), scaled(self.position[1] - 0.5), 0)

        glVertex(scaled(self.position[0] - 0.23), scaled(self.position[1] + 0.05), 0)
        glVertex(scaled(self.position[0] - 0.23), scaled(self.position[1] + 0.2), 0)
        glVertex(scaled(self.position[0] - 0.08), scaled(self.position[1] + 0.2), 0)
        glVertex(scaled(self.position[0] - 0.08), scaled(self.position[1] + 0.05), 0)

        glVertex(scaled(self.position[0] + 0.08), scaled(self.position[1] + 0.05), 0)
        glVertex(scaled(self.position[0] + 0.08), scaled(self.position[1] + 0.2), 0)
        glVertex(scaled(self.position[0] + 0.23), scaled(self.position[1] + 0.2), 0)
        glVertex(scaled(self.position[0] + 0.23), scaled(self.position[1] + 0.05), 0)

        glEnd()

    def fire(self):
        altPos = [scaled(self.position[0]), formated(scaled(self.position[1] - .75))]
        Bullets.add(altPos, -1)


class Enemies:

    def __init__(self):
        self.count = 24
        self.rows = 3
        self.perRow = self.count // self.rows
        self.list = [Enemy() for i in range(self.count)]
        self.position = [-7, 4]  # left bottom
        self.moveLimit = (-9, -5)  # left bottom [Xstart: Xend]
        self.moveDirection = 1
        self.moveStepTime = 1  # in seconds
        self.lastMoveTime = time.time()
        self.timeBetweenShots = 1.5  # in seconds
        self.lastShot = time.time()
        self.deadLine = -5

        self.generate()

    def generate(self):
        for j in range(self.rows):
            for i in range(self.perRow):
                self.list[i + self.perRow * j].position = [
                    self.position[0] + (i * 2),
                    self.position[1] + j * 2
                ]

    def updatePosition(self, position):
        self.position[0] += position[0]
        self.position[1] += position[1]

        for enemy in self.list:
            enemy.position[0] += position[0]
            enemy.position[1] += position[1]

    def draw(self):
        for enemy in self.list:
            enemy.draw()

            # Kill ship when the first enemy reaches deadline
            if enemy.position[1] == self.deadLine:
                Ship.die()
                time.sleep(0.5)
                return

        # Draw deadline
        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex3f(scaled(-10), scaled(self.deadLine), 0)
        glVertex3f(scaled(10), scaled(self.deadLine), 0)
        glEnd()

        self.move()
        self.randomShots()

    def move(self):
        if time.time() - self.lastMoveTime >= self.moveStepTime:

            if self.moveDirection == 0:
                self.updatePosition([0, -1])

                # update move direction
                if self.position[0] == self.moveLimit[0]:
                    self.moveDirection = 1
                elif self.position[0] == self.moveLimit[1]:
                    self.moveDirection = -1

            else:
                self.updatePosition([self.moveDirection, 0])

                # update move direction
                if (self.position[0] == self.moveLimit[0] or
                        self.position[0] == self.moveLimit[1]):
                    self.moveDirection = 0

            self.lastMoveTime = time.time()

    def kill(self, enemy):
        self.list.remove(enemy)
        Ship.increaseScore()

    def randomShots(self):
        if time.time() - self.lastShot >= self.timeBetweenShots:
            random.choice(self.list).fire()

            self.lastShot = time.time()

            # play sound
            playSFX('enemy-laser.wav')


class Bullet:

    def __init__(self, ownerPosition, direction=1):
        self.position = [ownerPosition[0], ownerPosition[1]]  # start position
        self.direction = direction
        self.lastMoveTime = time.time()
        self.speed = 0.035  # interval in seconds

    def draw(self):
        glColor3f(1, 1, 1)
        glTranslatef(
            self.position[0],
            self.position[1],
            0
        )
        glutSolidSphere(scaled(.1), 10, 10)
        glLoadIdentity()

    def updatePosition(self):
        if time.time() - self.lastMoveTime >= self.speed:
            self.position[1] += (self.direction * scaled(1))

            self.lastMoveTime = time.time()


class Bullets:
    list = []
    longetPath = 10

    @staticmethod
    def add(ownerPosition, direction=1):
        Bullets.list.append(Bullet(ownerPosition, direction))

    @staticmethod
    def trace(ship, enemies, blocks):
        for bullet in Bullets.list:

            # Collesion detection
            for enemy in enemies.list:
                scaledEnemyPos = [
                    scaled(enemy.position[0]),
                    scaled(enemy.position[1])
                ]

                if bullet.direction == 1:
                    if getDistance(bullet.position, scaledEnemyPos) < scaled(0.5):  # 0.5 is the width of enemy/2
                        enemies.kill(enemy)
                        Bullets.list.remove(bullet)
                        break
                elif bullet.direction == -1:
                    if getDistance(bullet.position, [ship.posX, ship.posY]) < scaled(0.75):
                        ship.loseLive()
                        Bullets.list.remove(bullet)
                        break

            for brick in blocks.list:
                scaledBrickPos = [
                    scaled(brick.position[0]),
                    scaled(brick.position[1])
                ]

                if getDistance(bullet.position, scaledBrickPos) <= scaled(.5):
                    Bullets.list.remove(bullet)
                    blocks.list.remove(brick)
                    break

            
            # remove bullet when it reaches the end of scene
            if (bullet.position[1] > scaled(Bullets.longetPath) or
                    bullet.position[1] < -1 * scaled(Bullets.longetPath)):
                Bullets.list.remove(bullet)
                continue

            bullet.draw()

        Bullets.updatePosition()

    @staticmethod
    def updatePosition():
        for bullet in Bullets.list:
            bullet.updatePosition()
