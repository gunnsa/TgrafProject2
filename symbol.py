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

        glBegin(GL_TRIANGLE_FAN)
        glColor3f(*self.color)
        glVertex2f(330,220) # (x1, y1)
        glVertex2f(350,200) # (x2, y1)
        glVertex2f(490,340) # (x2, y2)
        glVertex2f(470,360) # (x1, y2)
        glEnd()
        if self.type == "won":
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(330,220) # (x1, y2)
            glVertex2f(350,240) # (x1, y2)
            glVertex2f(300,290) # (x1, y2)
            glVertex2f(280,270) # (x1, y2)
            glEnd()
        elif self.type == "lost":
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(350,360) # (x1, y2)
            glVertex2f(330,340) # (x1, y2)
            glVertex2f(470,200) # (x1, y2)
            glVertex2f(490,220) # (x1, y2) ddd
            glEnd()

        glPopMatrix()


        # 200 = 330
        #