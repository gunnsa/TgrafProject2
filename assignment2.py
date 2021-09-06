import pygame
from pygame.locals import *

try:
    try:
        from OpenGL.GL import * # this fails in <=2020 versions of Python on OS X 11.x
    except ImportError:
        print('Drat, patching for Big Sur')
        from ctypes import util
        orig_util_find_library = util.find_library
        def new_util_find_library( name ):
            res = orig_util_find_library( name )
            if res: return res
            return '/System/Library/Frameworks/'+name+'.framework/'+name
        util.find_library = new_util_find_library
        from OpenGL.GL import *
except ImportError:
    pass
from OpenGL.GLU import *


x_pos_begin = None
x_pos_end = None
y_pos_begin = None
y_pos_end = None



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
            if event.button == 1: # left button -> rectangle
                x_pos_begin = pygame.mouse.get_pos()[0]
                y_pos_begin = max_y - pygame.mouse.get_pos()[1]
            elif event.button == 3: # right button -> line
                x_pos_begin = pygame.mouse.get_pos()[0]
                y_pos_begin = max_y - pygame.mouse.get_pos()[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # left button -> rectangle
                x_pos_end = pygame.mouse.get_pos()[0]
                y_pos_end = max_y - pygame.mouse.get_pos()[1]
            elif event.button == 3: # right button -> line
                x_pos_end = pygame.mouse.get_pos()[0]
                y_pos_end = max_y - pygame.mouse.get_pos()[1]
    update()
    display()


if __name__ == "__main__":
    init_game()
    while True:
        game_loop()
