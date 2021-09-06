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
    # color: tuple
    # angle: float
    # scale: Vector

    def draw(self):
        glPushMatrix()
        # print("Begin point: {}, {}".format(self.begin_position.x, self.begin_position.y))
        # print("End point: {}, {}".format(self.end_position.x, self.end_position.y))
        # glTranslate(self.positon.x, self.positon.y)
        # glScale(self.scale.x, self.scale.y , 1)

        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0.6, 1.0, 1.0)
        glVertex2f(self.begin_position.x, self.begin_position.y) # (x1, y1)
        glVertex2f(self.end_position.x, self.begin_position.y) # (x2, y1)
        glVertex2f(self.end_position.x, self.end_position.y) # (x2, y2)
        glVertex2f(self.begin_position.x, self.end_position.y) # (x1, y2)
        glEnd()

        # glRotate(self.angle, 0, 0, 1)

        glPopMatrix()