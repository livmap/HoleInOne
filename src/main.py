import pygame
import sys

from utilities import *
from golfball import *

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

# Load assets
background = loadImage("background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
ball = GolfBall(100, 100, 20, 20)
ball_image = loadImage("golfball.png", ball.w, ball.h)

# Clock settings
clock = pygame.time.Clock()
FPS = 60

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
                print("A button pressed!")

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
