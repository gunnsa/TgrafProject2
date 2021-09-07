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
    begin_position: Point

    def draw(self):
        triangles = 10
        radius = 1
    
        glPushMatrix()

        glBegin(GL_TRIANGLE_STRIP)
        glColor3f(0.6, 1.0, 1.0)
        glVertex2f(self.begin_position.x, self.begin_position.y) # (x1, y1)
        glEnd()

        glPopMatrix()