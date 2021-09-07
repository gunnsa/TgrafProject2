from dataclasses import dataclass

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from data import Vector
from data import Point


@dataclass
class Cannon:
    position: Point
    angle: float

    def draw(self):
        glPushMatrix()

        glTranslate(self.position.x, self.position.y, 0)
        glRotate(self.angle, 0, 0, 1)
        glTranslate(-self.position.x, -self.position.y, 0)

        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0.6, 1.0, 1.0)
        glVertex2f(self.position.x - 10, self.position.y) # (x1, y1)
        glVertex2f(self.position.x + 10, self.position.y) # (x2, y1)
        glVertex2f(self.position.x + 10, self.position.y + 70) # (x2, y2)
        glVertex2f(self.position.x - 10, self.position.y + 70) # (x1, y2)
        glEnd()


        glPopMatrix()