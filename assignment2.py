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

import math

from box import Box
from line import Line
from cannon import Cannon
from cannonball import Cannonball
from data import Point, Vector

x_pos_begin = None
x_pos_end = None
y_pos_begin = None
y_pos_end = None

ball_point = Point(400, 110)
cannonball = Cannonball(ball_point, Vector(0, 0))

cannon_point = Point(400,10)
cannon = Cannon(cannon_point, 0, cannonball)

goal_point1 = Point(300, 500)
goal_point2 = Point(500, 600)
goal = Box(goal_point1, goal_point2)

new_obstacle = None

going_left = False
going_right = False

max_x = 800
max_y = 600

size = 60

playing = False

objects = []

def init_game():
    pygame.display.init()
    pygame.display.set_mode((max_x, max_y), DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)


def update(clock):
    global going_left, going_right, cannon, max_y, playing
    delta_time = clock.tick(60) / 1000.0
    # if going_right:
    #     if cannon.end_position.x < 800:
    #         cannon.begin_position.x += 0.1
    #         cannon.end_position.x += 0.1
    # if going_left:
    #     if cannon.begin_position.x > 0:
    #         cannon.begin_position.x -= 0.1
    #         cannon.end_position.x -= 0.1
    if new_obstacle:
        pos = pygame.mouse.get_pos()
        new_end_point = Point(pos[0], max_y - pos[1])
        new_obstacle.end_position = new_end_point

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        if cannon.angle < 70:
            cannon.angle += delta_time * 100
    if pressed[pygame.K_RIGHT]:
        if cannon.angle > -70:
            cannon.angle -= delta_time * 50
    if pressed[pygame.K_z]:
        if not playing:
            cannon.child = None

            new_cannon_point_x = cannon.position.x + (100 * math.cos((cannon.angle + 90) * (math.pi/180)))
            new_cannon_point_y = cannon.position.y + (100 * math.sin((cannon.angle + 90) * (math.pi/180)))
            new_cannon_point = Point(new_cannon_point_x, new_cannon_point_y)

            motion = Vector(-math.sin(cannon.angle * (math.pi / 180)), math.cos(cannon.angle * (math.pi / 180)))

            cannonball.position = new_cannon_point
            cannonball.motion = motion
            playing = True


def display():
    global objects, cannon, cannonball
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glViewport(0, 0, 800, 600)
    gluOrtho2D(0, 800, 0, 600)

    cannon.draw()
    goal.draw()

    if cannon.child == None:
        cannonball.draw()
        cannonball.update()

    if new_obstacle:
        new_obstacle.draw()

    for object in objects:
        object.draw()

    pygame.display.flip()


def game_loop():
    global objects, x_pos_begin, y_pos_begin, x_pos_end, y_pos_end
    global going_left, going_right, new_obstacle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()
        #     if event.key == K_LEFT:
        #         going_left = True
        #     if event.key == K_RIGHT:
        #         going_right = True
        # if event.type == pygame.KEYUP:
        #     if event.key == K_LEFT:
        #         going_left = False
        #     if event.key == K_RIGHT:
        #         going_right = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left button -> rectangle
                x_pos_begin = pygame.mouse.get_pos()[0]
                y_pos_begin = max_y - pygame.mouse.get_pos()[1]
                point = Point(x_pos_begin, y_pos_begin)
                new_obstacle = Box(point, point)
            elif event.button == 3: # right button -> line
                x_pos_begin = pygame.mouse.get_pos()[0]
                y_pos_begin = max_y - pygame.mouse.get_pos()[1]
                point = Point(x_pos_begin, y_pos_begin)
                new_obstacle = Line(point, point)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # left button -> rectangle
                x_pos_end = pygame.mouse.get_pos()[0]
                y_pos_end = max_y - pygame.mouse.get_pos()[1]
                objects.append(new_obstacle)
                new_obstacle = None
            elif event.button == 3: # right button -> line
                x_pos_end = pygame.mouse.get_pos()[0]
                y_pos_end = max_y - pygame.mouse.get_pos()[1]
                objects.append(new_obstacle)
                new_obstacle = None
    clock = pygame.time.Clock()
    update(clock)
    display()


if __name__ == "__main__":
    init_game()
    while True:
        game_loop()
