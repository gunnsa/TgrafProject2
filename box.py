from dataclasses import dataclass

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from data import Vector
from data import Point


@dataclass
class Box:
    begin_position: Point
    end_position: Point
    # motion: Vector
    # size: Vector
    color: tuple
    # scale: Vector

    def draw(self):
        glPushMatrix()

        glBegin(GL_TRIANGLE_FAN)
        glColor3f(*self.color)
        glVertex2f(self.begin_position.x, self.begin_position.y) # (x1, y1)
        glVertex2f(self.end_position.x, self.begin_position.y) # (x2, y1)
        glVertex2f(self.end_position.x, self.end_position.y) # (x2, y2)
        glVertex2f(self.begin_position.x, self.end_position.y) # (x1, y2)
        glEnd()

        glPopMatrix()