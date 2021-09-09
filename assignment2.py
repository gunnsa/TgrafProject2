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
cannonball = Cannonball(ball_point, Vector(0, 0), ball_point)

cannon_point = Point(400,10)
cannon = Cannon(cannon_point, 0, cannonball)

goal_point1 = Point(300, 500)
goal_point2 = Point(500, 600)
goal = Box(goal_point1, goal_point2)

new_obstacle = None

max_x = 800
max_y = 600

size = 60

playing = False

obstacles = []

def init_game():
    pygame.display.init()
    pygame.display.set_mode((max_x, max_y), DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)


def collision_detector(delta_time):
    # dynamic check for single point crossing diagonal line
    # Use formula for intersection of ray with line (explained in “Examples 1” on lecture page)
    # When t.hit is found, check if that time is within the current frame (between 0 and deltaTime)
    # If so, check to see if P.hit is between the end points of the line
    # If so, collision happened!

    # for all obsticles
    #   check if cannonball collides
    #   if so: bounce back
    global cannonball, obstacles, playing
    #delta_time = clock.tick(60) / 1000.0
    lines = []
    if playing:
        for obstacle in obstacles:
            # print(type(obstacle))
            if isinstance(obstacle, Box):
                # print("box")
                point1 = Point(obstacle.begin_position.x, obstacle.begin_position.y)
                point2 = Point(obstacle.begin_position.x, obstacle.end_position.y)
                point3 = Point(obstacle.end_position.x, obstacle.end_position.y)
                point4 = Point(obstacle.end_position.x, obstacle.begin_position.y)

                lines.append(Line(point1, point2))
                lines.append(Line(point2, point3))
                lines.append(Line(point3, point4))
                lines.append(Line(point4, point1))

                # print("obstacle begin pos: ({}, {}) - obstacle end pos: ({}, {})".format(obstacle.begin_position.x, obstacle.begin_position.y, obstacle.end_position.x, obstacle.end_position.y))

                # print("Point1 : ({},{})".format(point1.x, point1.y))
                # print("Point2 : ({},{})".format(point2.x, point2.y))
                # print("Point3 : ({},{})".format(point3.x, point3.y))
                # print("Point4 : ({},{})".format(point4.x, point4.y))

                # print("Cannonball position: ({}, {})".format(cannonball.position.x, cannonball.position.y))
            if isinstance(obstacle, Line):
                # print("line")
                lines.append(obstacle)
        for index, line in enumerate(lines):
            print("line {} begin pos: ({}, {}) - line end pos: ({}, {})".format(index, line.begin_position.x, line.begin_position.y, line.end_position.x, line.end_position.y))
            n = Vector(-1 * (line.end_position.y - line.begin_position.y), line.end_position.x - line.begin_position.x)
            print("n: ({}, {})".format(n.x, n.y))
            # print("cannonball motion vector: ({}, {})".format(cannonball.motion.x, cannonball.motion.y))
            b_min_a = Vector(line.begin_position.x - cannonball.position.x, line.begin_position.y - cannonball.position.y)
            # b_min_a = Point(line.begin_position.x - cannonball.position.x, line.begin_position.y - cannonball.position.y)
            ndotba = (n.x * b_min_a.x) + (n.y * b_min_a.y)
            print(ndotba)
            ndotmotion = (n.x * cannonball.motion.x) + (n.y * cannonball.motion.y)
            print(ndotmotion)
            thit = ndotba / ndotmotion
            print(thit)
            # t_hit = ((n.x * b_min_a.x) + (n.y * b_min_a.y)) / ((n.x * cannonball.motion.x) + (n.y * cannonball.motion.y))
            # print("line {} - t hit: {}".format(index, t_hit))
            # print('time', delta_time)
            # print("t_hit: {}".format(t_hit))
            if thit >= 0 and thit <= delta_time:
                print("COLLISION")
                pass

            t_hit_times_c = Point(thit * cannonball.motion.x, thit * cannonball.motion.y)
            p_hit = Point(400 + t_hit_times_c.x, 110 + t_hit_times_c.y)

            # print("p hit: ({}, {})".format(p_hit.x, p_hit.y))
            # print("cannonball pos: ({}, {})".format(cannonball.position.x, cannonball.position.y))
            # print("cannonball pos: ({}, {})".format(cannonball.prevposition.x, cannonball.prevposition.y))

            if cannonball.prevposition.x <= p_hit.x and cannonball.position.x >= p_hit.x and cannonball.prevposition.y <= p_hit.y and cannonball.position.y >= p_hit.y:
                print("YAY")

def update(clock):
    delta_time = clock.tick(60) / 1000.0
    # print('time', delta_time)

    collision_detector(delta_time)
    global cannon, max_y, playing
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
            cannon.angle -= delta_time * 100
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
    global obstacles, cannon, cannonball
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

    for obstacle in obstacles:
        obstacle.draw()

    pygame.display.flip()


def game_loop():
    global obstacles, x_pos_begin, y_pos_begin, x_pos_end, y_pos_end, new_obstacle
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
                obstacles.append(new_obstacle)
                new_obstacle = None
            elif event.button == 3: # right button -> line
                x_pos_end = pygame.mouse.get_pos()[0]
                y_pos_end = max_y - pygame.mouse.get_pos()[1]
                obstacles.append(new_obstacle)
                new_obstacle = None
    clock = pygame.time.Clock()
    update(clock)
    display()


if __name__ == "__main__":
    init_game()
    while True:
        game_loop()
