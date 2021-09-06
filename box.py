from dataclasses import dataclass

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from dataclasses import Vector
from dataclasses import Point


@dataclass
class Box:
    positon: Point
    # motion: Vector
    size: Vector
    color: tuple
    angle: float
    scale: Vector

    def draw(self):
        glPushMatrix()

        glTranslate(self.positon.x, self.positon.y)
        glScale(self.scale.x, self.scale.y , 1)

        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0.6, 1.0, 1.0)
        glVertex2f(self.size.x/2, self.size.y/2)
        glVertex2f(self.size.x/2, self.size.y/2)
        glVertex2f(self.size.x/2, self.size.y/2)
        glVertex2f(self.size.x/2, self.size.y/2)
        glEnd()
        glRotate(self.angle, 0, 0, 1)

        glPopMatrix()