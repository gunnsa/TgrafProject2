from dataclasses import dataclass

import math

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from data import Vector
from data import Point


@dataclass
class Cannonball:
    position: Point
    motion: Vector

    def draw(self):
        _theta = 0
        radius = 18
        theta = (_theta-90) * math.pi/180
        glPushMatrix()

        glBegin(GL_TRIANGLE_STRIP)
        x = self.position.x + (radius * math.cos(theta))
        y = self.position.y + (radius * math.sin(theta))
        glVertex2f(x, y)

        _theta += 10
        theta = (_theta-90) * math.pi/180

        while theta <= 360:
            theta = (_theta-90) * math.pi/180
            x = self.position.x + (radius * math.cos(theta))
            y = self.position.y + (radius * math.sin(theta))
            glVertex2f(x, y)
            glVertex2f(self.position.x, self.position.y) # center point
            _theta += 10

        glColor3f(0.6, 1.0, 1.0)
        glEnd()

        glPopMatrix()

    def update(self):
        self.position.x += (self.motion.x * 5)
        self.position.y += (self.motion.y * 5)