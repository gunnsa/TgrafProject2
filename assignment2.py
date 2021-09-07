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

point1 = Point(350,10)
point2 = Point(450,30)
cannon = Box(point1, point2)

going_left = False
going_right = False

max_x = 800
max_y = 600

size = 60

objects = []

def init_game():
    pygame.display.init()
    pygame.display.set_mode((max_x, max_y), DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)


def update():
    global going_left, going_right, cannon
    if going_right:
        if cannon.end_position.x < 800:
            cannon.begin_position.x += 0.1
            cannon.end_position.x += 0.1
    if going_left:
        if cannon.begin_position.x > 0:
            cannon.begin_position.x -= 0.1
            cannon.end_position.x -= 0.1

def display():
    global objects, cannon
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glViewport(0, 0, 800, 600)
    gluOrtho2D(0, 800, 0, 600)

    cannon.draw()

    for object in objects:
        object.draw()

    pygame.display.flip()


def game_loop():
    global objects, x_pos_begin, y_pos_begin, x_pos_end, y_pos_end
    global going_left, going_right
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
