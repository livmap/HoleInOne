import pygame
import sys
import math
import random

from utilities import *
from golfball import *
from world import *
from aimAssist import *
from hole import *
from obstacle import *

# Initialize Pygame and joystick module
pygame.init()
pygame.joystick.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Boilerplate")

# Classes

world = World(0.08)

ball = GolfBall(100, SCREEN_HEIGHT / 2, 20, 20)
ball.setHitVelocity(15)

aimAssist = AimAssist(50, 50, 0, 5, WHITE)

# Load assets
background = loadImage("background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

ball_images = []
ball_images.append(loadImage("golfball1.png", ball.w, ball.h))
ball_images.append(loadImage("golfball2.png", ball.w, ball.h))
ball_image = ball_images[0]

hole = Hole(900, random.randint(50, SCREEN_HEIGHT - 50), 25, 25)
hole_img = loadImage("hole.png", hole.w, hole.h)

obstacle = Obstacle(500, 400, w=50)
obstacle_img = loadImage("obstacle.png", obstacle.w, obstacle.h)

# Clock settings
clock = pygame.time.Clock()
FPS = 60

rect_surface = pygame.Surface((100, 100))  # Transparent surface
angle = 0


# Initialize the Xbox controller
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Connected joystick: {joystick.get_name()}")
else:
    print("No joystick detected!")
    joystick = None

running = True
play = True

count = 0

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Joystick button press handling
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # A button is usually button 0 on Xbox controllers
                if ball.getVelocity() == 0 and play:
                    ball.vX = ball.hitVelocity * (axis_x / math.hypot(axis_x, axis_y)) * (math.hypot(axis_x, axis_y) / 1)
                    ball.vY = ball.hitVelocity * (axis_y / math.hypot(axis_x, axis_y)) * (math.hypot(axis_x, axis_y) / 1)
                    ball.xRatio = (axis_x / math.hypot(axis_x, axis_y))
                    ball.yRatio = (axis_y / math.hypot(axis_x, axis_y))

    if play:
        ball.x += ball.vX
        ball.y += ball.vY

    # Applying Friction
    veloc = ball.getVelocity()
    if veloc >= world.friction:
        veloc -= world.friction
        ball.vX = veloc * ball.xRatio
        ball.vY = veloc * ball.yRatio
    else:
        ball.vX = 0
        ball.vY = 0

    if ball.x < 0:
        ball.xRatio = abs(ball.xRatio)

    if ball.x > (SCREEN_WIDTH - ball.w):
        ball.xRatio = -(abs(ball.xRatio))

    if ball.y < 0:
        ball.yRatio = abs(ball.yRatio)

    if ball.y > (SCREEN_HEIGHT - ball.h):
        ball.yRatio = -(abs(ball.yRatio))

    # Joystick axis movement (e.g., move ball with left joystick)
    if joystick:
        axis_x = joystick.get_axis(0)  
        axis_y = joystick.get_axis(1)  

    # Drawing
    screen.blit(background, (0, 0))
    if ball.getVelocity() > 1:
        num = int(count / (ball.hitVelocity - ball.getVelocity()))  % 2
        ball_image = ball_images[num]
    
    screen.blit(hole_img, (hole.x, hole.y))
    if cartesian(ball.x, ball.y, hole.x, hole.y) < ((hole.w / 2) + (ball.w / 2)):
        play = False

    screen.blit(obstacle_img, (obstacle.x, obstacle.y))

    hit = collision(ball.x + (ball.w / 2), ball.y + (ball.h / 2), ball.w / 2, obstacle.x, obstacle.y, obstacle.w, obstacle.h)
    if hit[0]:
        s = hit[1]
        if s == 1:
            ball.xRatio = -(abs(ball.xRatio))
        elif s == 2:
            ball.yRatio = -(abs(ball.yRatio))
        elif s == 3:
            ball.xRatio = (abs(ball.xRatio))
        elif s == 4:
            ball.yRatio = abs(ball.yRatio)

    if play:
        screen.blit(ball_image, (ball.x, ball.y))

    # Update display
    pygame.display.flip()

    count += 1

    # Control the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
