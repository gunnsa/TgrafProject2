import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


x_pos = None
y_pos = None

max_x = 800
max_y = 600

size = 60

square = [];

def init_game():
    pygame.display.init()
    pygame.display.set_mode((max_x, max_y), DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)


def update():
    global square
    if x_pos and y_pos:
        square.append([x_pos - (size/2), y_pos - (size/2), x_pos + (size/2), y_pos + (size/2)]) #x1, y1, x2, y2


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glViewport(0, 0, 800, 600)
    gluOrtho2D(0, 800, 0, 600)
    for coordinate in square:
        glBegin(GL_POLYGON)
        glColor3f(0.6, 1.0, 1.0)
        glVertex2f(coordinate[0], coordinate[1])#x1 ,y1
        glVertex2f(coordinate[2], coordinate[1])#x2, y1
        glVertex2f(coordinate[2], coordinate[3])#x2, y2
        glVertex2f(coordinate[0], coordinate[3])#x1, y2
        glEnd()

    pygame.display.flip()


def game_loop():
    global x_pos, y_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x_pos = pygame.mouse.get_pos()[0]
                y_pos = max_y - pygame.mouse.get_pos()[1]
    update()
    display()


if __name__ == "__main__":
    init_game()
    while True:
        game_loop()
