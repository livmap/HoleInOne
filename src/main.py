import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Boilerplate")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


clock = pygame.time.Clock()
FPS = 60  

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)  

    pygame.display.flip()


    clock.tick(FPS)

pygame.quit()
sys.exit()