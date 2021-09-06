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

from box import Box
from line import Line
from data import Point, Vector

x_pos_begin = None
x_pos_end = None
y_pos_begin = None
y_pos_end = None

max_x = 800
max_y = 600

size = 60

objects = []

def init_game():
    pygame.display.init()
    pygame.display.set_mode((max_x, max_y), DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)


def update():
    global square
    # if x_pos and y_pos:
    #     square.append([x_pos - (size/2), y_pos - (size/2), x_pos + (size/2), y_pos + (size/2)]) #x1, y1, x2, y2

def display():
    global objects
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glViewport(0, 0, 800, 600)
    gluOrtho2D(0, 800, 0, 600)

    point1 = Point(350,0)
    point2 = Point(450,20)
    cannon = Box(point1, point2)
    cannon.draw()

    for object in objects:
        object.draw()
        # glBegin(GL_POLYGON)
        # glColor3f(0.6, 1.0, 1.0)
        # glVertex2f(coordinate[0], coordinate[1])#x1 ,y1
        # glVertex2f(coordinate[2], coordinate[1])#x2, y1
        # glVertex2f(coordinate[2], coordinate[3])#x2, y2
        # glVertex2f(coordinate[0], coordinate[3])#x1, y2
        # glEnd()

    pygame.display.flip()


def game_loop():
    global objects, x_pos_begin, y_pos_begin, x_pos_end, y_pos_end
    for event in pygame.event.get():
        point1 = None
        point2 = None
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == K_LEFT:
                going_left = True
            if event.key == K_RIGHT:
                going_right = True
        if event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                going_left = False
            if event.key == K_RIGHT:
                going_right = False
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
                point1 = Point(x_pos_begin, y_pos_begin)
                point2 = Point(x_pos_end, y_pos_end)
                box = Box(point1, point2)
                objects.append(box)
            elif event.button == 3: # right button -> line
                x_pos_end = pygame.mouse.get_pos()[0]
                y_pos_end = max_y - pygame.mouse.get_pos()[1]
                point1 = Point(x_pos_begin, y_pos_begin)
                point2 = Point(x_pos_end, y_pos_end)
                line = Line(point1, point2)
                objects.append(line)
    update()
    display()


if __name__ == "__main__":
    init_game()
    while True:
        game_loop()
