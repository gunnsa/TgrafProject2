from dataclasses import dataclass

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from data import Point


@dataclass
class Symbol:
    color: tuple
    type: str

    def draw(self):
        # print("drawing symbol")
        glPushMatrix()

        glBegin(GL_POLYGON)
        glColor3f(*self.color)
        glVertex2f(250,400) # (x1, y1)
        glVertex2f(350,300) # (x2, y1)
        glVertex2f(550,500) # (x2, y2)
        glVertex2f(500,550) # (x1, y2)
        glVertex2f(350,350) # (x1, y2)
        glVertex2f(250,450) # (x1, y2)
        glEnd()

        glPopMatrix()