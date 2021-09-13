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
from symbol import Symbol
from data import Point, Vector

# Color constants
BLACK = (0.0, 0.0, 0.0)
GREEN = (0.5, 1.0, 0.5)
RED = (1.0, 0.0, 0.0)

x_pos_begin = None
x_pos_end = None
y_pos_begin = None
y_pos_end = None

obstacles = []
new_obstacle = None

symbol = None

max_x = 800
max_y = 600

playing = False
game_won = False


def init_game():
    pygame.display.init()
    pygame.display.set_mode((max_x, max_y), DOUBLEBUF | OPENGL)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    reset_game()

def reset_game():
    global obstacles, cannonball, cannon, goal, symbol, playing, game_won
    playing = False
    game_won = False
    obstacles = []
    obstacles.append(Box(Point(0, 30), Point(3, 570), BLACK)) # Left side border
    obstacles.append(Box(Point(30, 597), Point(770, 600), BLACK)) # Top left border
    obstacles.append(Box(Point(297, 600), Point(300, 550), BLACK)) # Left goal border
    obstacles.append(Box(Point(297, 547), Point(380, 550), BLACK)) # Left bottom border on goal
    obstacles.append(Box(Point(420, 547), Point(503, 550), BLACK)) # Right bottom border on goal
    obstacles.append(Box(Point(500, 550), Point(503, 600), BLACK)) # Right goal border
    obstacles.append(Box(Point(797, 30), Point(800, 570), BLACK)) # Right border
    obstacles.append(Box(Point(390, 298), Point(410, 301), BLACK)) # Border in middle of screen to prevent gamer from cheating
    obstacles.append(Box(Point(30, 0), Point(770, 3), BLACK)) # Bottom border

    ball_point = Point(400, 100)
    cannonball = Cannonball(ball_point, Vector(0, 0), ball_point)

    cannon_point = Point(400,10)
    cannon = Cannon(cannon_point, 0, cannonball)

    goal_point1 = Point(300, 550)
    goal_point2 = Point(500, 597)
    goal = Box(goal_point1, goal_point2, GREEN)

def check_inside_box(box, point):
    global game_won, playing
    if point.x > box.begin_position.x and point.x < box.end_position.x and point.y > box.begin_position.y and point.y < box.end_position.y:
        # print("You won")
        game_won = True
        playing = False
        return True


def check_out_of_bounds(ball):
    global playing
    if ball.position.x < 0 or ball.position.x > 800:
        playing = False
        return True
    if ball.position.y < 0 or ball.position.y > 600:
        playing = False
        return True


def check_on_line(line, point):
    horizontal_line = line.begin_position.y == line.end_position.y
    vertical_line = line.begin_position.x == line.begin_position.x

    if horizontal_line:
        if (line.begin_position.x <= point.x and line.end_position.x >= point.x) or \
            (line.end_position.x <= point.x and line.begin_position.x >= point.x):
            return True
    elif vertical_line:
        if (line.begin_position.y <= point.y and line.end_position.y >= point.y) or \
            (line.end_position.y <= point.y and line.begin_position.y >= point.y):
            return True
    else:
        negative_line = (line.begin_position.y - line.end_position.y)/(line.begin_position.x - line.end_position.x) < 0
        if negative_line and (line.begin_position.y >= point.y and line.end_position.y <= point.y and line.begin_position.x <= point.x and line.end_position.x >= point.x) or \
            (line.begin_position.y <= point.y and line.end_position.y >= point.y and line.begin_position.x >= point.x and line.end_position.x <= point.x):
            return True
        elif (line.begin_position.x <= point.x and line.end_position.x >= point.x and line.begin_position.y <= point.y and line.end_position.y >= point.y) or \
            (line.begin_position.x >= point.x and line.end_position.x <= point.x and line.begin_position.y >= point.y and line.end_position.y <= point.y):
            return True


def collision_detector(delta_time):
    global cannonball, obstacles, playing
    lines = []
    if playing:
        for obstacle in obstacles:
            if isinstance(obstacle, Box):
                point1 = Point(obstacle.begin_position.x, obstacle.begin_position.y)
                point2 = Point(obstacle.end_position.x, obstacle.begin_position.y)
                point3 = Point(obstacle.end_position.x, obstacle.end_position.y)
                point4 = Point(obstacle.begin_position.x, obstacle.end_position.y)

                lines.append(Line(point1, point2))
                lines.append(Line(point2, point3))
                lines.append(Line(point3, point4))
                lines.append(Line(point4, point1))

            if isinstance(obstacle, Line):
                lines.append(obstacle)
        for line in lines:
            n = Vector(-1 * (line.end_position.y - line.begin_position.y), line.end_position.x - line.begin_position.x)
            b_min_a = Vector(line.begin_position.x - cannonball.position.x, line.begin_position.y - cannonball.position.y)
            ndotba = (n.x * b_min_a.x) + (n.y * b_min_a.y)
            ndotmotion = (n.x * cannonball.motion.x) + (n.y * cannonball.motion.y)
            if ndotmotion == 0:
                ndotmotion = 1
            thit = ndotba / ndotmotion
            if thit >= 0 and thit < delta_time:
                t_hit_times_c = Point(thit * cannonball.motion.x, thit * cannonball.motion.y)
                p_hit = Point(cannonball.position.x + t_hit_times_c.x, cannonball.position.y + t_hit_times_c.y)
                if check_on_line(line, p_hit):
                    two_c_dot_n = (2 * (cannonball.motion.x * n.x) + 2 * (cannonball.motion.y * n.y))
                    n_dot_n = (n.x * n.x) + (n.y * n.y)
                    divide = two_c_dot_n / n_dot_n
                    divide_dot_n = Point(divide * n.x, divide * n.y)
                    r = Vector(cannonball.motion.x - divide_dot_n.x, cannonball.motion.y - divide_dot_n.y)
                    cannonball.motion = r


def update(clock):
    global cannon, max_y, playing, goal, cannonball, game_won, symbol
    delta_time = clock.tick(60) / 1000.0

    if check_inside_box(goal, cannonball.position):
        symbol = Symbol(GREEN, "won")
        symbol.draw()
        reset_game()
    elif check_out_of_bounds(cannonball):
        symbol = Symbol(RED, "lost")
        symbol.draw()
        reset_game()
    else:
        collision_detector(delta_time)

        if new_obstacle:
            symbol = None
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
    if pressed[pygame.K_r]:
        reset_game()
    if pressed[pygame.K_z]:
        if not playing:
            cannon.child = None
            symbol = None
            new_cannon_point_x = cannon.position.x + (100 * math.cos((cannon.angle + 90) * (math.pi/180)))
            new_cannon_point_y = cannon.position.y + (100 * math.sin((cannon.angle + 90) * (math.pi/180)))
            new_cannon_point = Point(new_cannon_point_x, new_cannon_point_y)

            motion = Vector((-math.sin(cannon.angle * (math.pi / 180)) + cannonball.motion.x) * 400, (math.cos(cannon.angle * (math.pi / 180)) + cannonball.motion.y) * 400)

            cannonball.position = new_cannon_point
            cannonball.motion = motion

            playing = True


def display(clock):
    delta_time = clock.tick(60) / 1000.0

    global obstacles, cannon, cannonball, symbol
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
        cannonball.update(delta_time)

    if new_obstacle:
        new_obstacle.draw()

    if symbol:
        symbol.draw()

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
                new_obstacle = Box(point, point, (0.439216, 0.576471, 0.858824))
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
    display(clock)


if __name__ == "__main__":
    init_game()
    while True:
        game_loop()
