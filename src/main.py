import pygame
import sys
import math

from utilities import *
from golfball import *
from world import *
from aimAssist import *

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

ball = GolfBall(100, 100, 20, 20)
ball.setHitVelocity(10)

aimAssist = AimAssist(50, 50, 0, 5, WHITE)

# Load assets
background = loadImage("background.png", SCREEN_WIDTH, SCREEN_HEIGHT)


ball_image = loadImage("golfball.png", ball.w, ball.h)

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

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Joystick button press handling
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # A button is usually button 0 on Xbox controllers
                if ball.getVelocity() == 0:
                    ball.vX = ball.hitVelocity * (axis_x / math.hypot(axis_x, axis_y)) * (math.hypot(axis_x, axis_y) / 1)
                    ball.vY = ball.hitVelocity * (axis_y / math.hypot(axis_x, axis_y)) * (math.hypot(axis_x, axis_y) / 1)
                    ball.xRatio = (axis_x / math.hypot(axis_x, axis_y))
                    ball.yRatio = (axis_y / math.hypot(axis_x, axis_y))

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

    # Joystick axis movement (e.g., move ball with left joystick)
    if joystick:
        axis_x = joystick.get_axis(0)  
        axis_y = joystick.get_axis(1)  

    # Drawing
    screen.blit(background, (0, 0))
    screen.blit(ball_image, (ball.x, ball.y))

    # Update display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
