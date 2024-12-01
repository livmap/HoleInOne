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
from sandPatch import *
from holeLevel import *

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
pygame.display.set_caption("HoleInOne")

# Starter Screen

logoWidth = 300
logoHeight = logoWidth / 2
logoX = (SCREEN_WIDTH - logoWidth) / 2
logoY = 100

buttonImageWidth = 200
buttonImageHeight = buttonImageWidth / 2
buttonImageX = (SCREEN_WIDTH - buttonImageWidth) / 2
def buttonImageY(num):
    return 200 + (100 * num)

logos = []
logos.append(loadImage("logo1.png", logoWidth, logoHeight))
logos.append(loadImage("logo2.png", logoWidth, logoHeight))
play_img = loadImage("play.png", buttonImageWidth, buttonImageHeight)
exit_img = loadImage("exit.png", buttonImageWidth, buttonImageHeight)

starter_img = loadImage("starter_back.png", SCREEN_WIDTH, SCREEN_HEIGHT)


# Classes

friction = 0.08
world = World(friction, random.randint(0, 8), random.randint(0, 359), True)


ball = GolfBall(100, SCREEN_HEIGHT / 2, 20, 20)
ball.setHitVelocity(15)

hole = Hole(900, random.randint(50, SCREEN_HEIGHT - 50), 25, 25)

obstacle = Obstacle(500, 400, w=50)

sandPatch = SandPatch(random.randint(100, SCREEN_WIDTH - 100), random.randint(50, SCREEN_HEIGHT - 50), random.randint(50, 100), random.randint(50, 100))

# Load assets
background = loadImage("background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

ball_images = []
ball_images.append(loadImage("golfball1.png", ball.w, ball.h))
ball_images.append(loadImage("golfball2.png", ball.w, ball.h))
ball_image = ball_images[0]

hole_img = loadImage("hole.png", hole.w, hole.h)

obstacle_img = loadImage("obstacle.png", obstacle.w, obstacle.h)

windArrow_img = loadImage("windArrow.png", 25, (25 / 266) * 500)
windArrow_img = pygame.transform.rotate(windArrow_img, -world.windDirection)

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

font = pygame.font.Font('freesansbold.ttf', 15)
text = font.render(str(world.windSpeed) + " / " + str(world.windDirection), True, BLACK)
textRect = text.get_rect()
textRect.center = (900, 50)


textRect2 = text.get_rect()
textRect2.center = (100, 50)

textRect3 = text.get_rect()
textRect3.center = (200, 50)

textRect4 = text.get_rect()
textRect4.center = (300, 50)

textRect5 = text.get_rect()
textRect5.center = (400, 50)

running = True
ended = False
started = False
play = False

count = 0


holeCount = 0
hits = 0
total_hits = 0
holeLevel = None
obstacles = []
sandPatches = []
noPlayCount = 0
least = None
most = 0 
best = 100000000
beaten = False

def gameInit():

    global ended
    global started
    global obstacles
    global sandPatches
    global play
    global holeCount
    global hits
    global ball
    global holeLevel
    global least
    global most
    global best
    global beaten
    global text
    global textRect
    global textRect2
    global textRect3
    global textRect4
    global textRect5
    

    font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render(str(world.windSpeed) + " / " + str(world.windDirection), True, BLACK)
    textRect = text.get_rect()
    textRect.center = (900, 50)


    textRect2 = text.get_rect()
    textRect2.center = (100, 50)

    textRect3 = text.get_rect()
    textRect3.center = (200, 50)

    textRect4 = text.get_rect()
    textRect4.center = (300, 50)

    textRect5 = text.get_rect()
    textRect5.center = (400, 50)

    if holeCount < 2:

        if holeCount == 0:
            least = 100000000
        else:
            if hits < least:
                least = hits
            
        if hits > most:
            most = hits

        ball.x = 100
        ball.y = SCREEN_HEIGHT / 2
        ball.vX = 0
        ball.vY = 0
        ball.xRatio = 0
        ball.yRatio = 0

        play = True
        holeCount += 1
        obstacles = []
        sandPatches = []
        hits = 0
        holeMove = False
        holeMoveVeloc = 0
        holeMoveRange = 0
        obstacleCount = random.randint(1, 10)
        sandPatchCount = random.randint(1, 5)
        parSum = 0

        for x in range(obstacleCount):
            obstacles.append(Obstacle(random.randint(100, SCREEN_WIDTH - 200), random.randint(50, SCREEN_HEIGHT - 50), 50))

        for y in range(sandPatchCount):
            sandPatches.append(SandPatch(random.randint(100, SCREEN_WIDTH - 200), random.randint(50, SCREEN_HEIGHT - 50), random.randint(50, 100), random.randint(50, 100)))

        holeMoveGuess = random.randint(0, 8000) % 2
        if holeMoveGuess == 0:
            holeMove = False
        else:
            holeMove = True

        if holeMove:
            holeMoveVeloc = random.randint(1, 10)
            holeMoveRange = random.randint(100, 300)

        if holeMove:
            parSum += 5

        parSum += obstacleCount + sandPatchCount

        par = round(parSum / 4)

        holeLevel = HoleLevel(sandPatchCount, obstacleCount, holeMove, par, holeMoveRange, holeMoveVeloc)

        hole.x = SCREEN_WIDTH - 100
        hole.y = random.randint(50, SCREEN_HEIGHT - 50)
    else:

        if hits < least:
                least = hits

        if hits > most:
            most = hits

        file = open("/Users/princemaphupha/Desktop/Games/HoleInOne/src/games.txt", "r")
        lines = file.readlines()
        scores = []
        res = []
        
        for sub in lines:
            res.append(sub.replace("\n", ""))
        for w in res:
            scores.append(int(w))

        for x in scores:
            if x < best:
                best = x
        
        if total_hits < best:
            beaten = True
            best = total_hits

        file.close()
        file = open("/Users/princemaphupha/Desktop/Games/HoleInOne/src/games.txt", "a")
        file.write(str(total_hits) + "\n")
        file.close()
        started = False
        ended = True


while running:
    if started:
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
                        hits += 1
                        total_hits += 1

        if not play:
            gameInit()

        if play:
            ball.x += ball.vX
            ball.y += ball.vY
            if ball.getVelocity() > 0:
                if ball.x > 0 and ball.x < SCREEN_WIDTH - ball.w:
                    ball.x += (world.windSpeed / 5)  * math.cos(world.windDirection)
                if ball.y > 0 and ball.y < SCREEN_HEIGHT - ball.h:
                    ball.y += (world.windSpeed / 5) * math.sin(world.windDirection)
                
            
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
        
        
        if cartesian(ball.x + (ball.w  / 2), ball.y + (ball.h / 2), hole.x + (hole.w / 2), hole.y + (hole.h / 2)) < ((hole.w / 2) + (ball.w / 2)):
            play = False
        

        for y in sandPatches:
            pygame.draw.rect(screen, y.color, (y.x, y.y, y.w, y.h))

            hitSand = collision(ball.x + (ball.w / 2), ball.y + (ball.h / 2), ball.w / 2, y.x, y.y, y.w, y.h)
            if hitSand[0]:
                world.friction = world.friction * 2
            else:
                if world.rain:
                    world.friction = friction * 0.75
                else:
                    world.friction = friction

        for x in obstacles:
            screen.blit(obstacle_img, (x.x, x.y))
            hitObs = collision(ball.x + (ball.w / 2), ball.y + (ball.h / 2), ball.w / 2, x.x, x.y, x.w, x.h)
            if hitObs[0]:
                s = hitObs[1]
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
            
        
        screen.blit(hole_img, (hole.x, hole.y))
        screen.blit(windArrow_img, (800, 50))
        text2 = font.render("Hole: " + str(holeCount), True, BLACK)
        text3 = font.render("Par: " + str(holeLevel.par), True, BLACK)
        text4 = font.render("Hits: " + str(hits), True, BLACK)
        text5 = font.render("Total Hits: " + str(total_hits), True, BLACK)
        screen.blit(text, textRect)
        screen.blit(text2, textRect2)
        screen.blit(text3, textRect3)
        screen.blit(text4, textRect4)
        screen.blit(text5, textRect5)
        

        # Update display
        pygame.display.flip()

        count += 1

        # Control the frame rate
        clock.tick(FPS)

    else:
        if not ended:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Set the x, y postions of the mouse click
                    x, y = event.pos
                    if x > buttonImageX and x < buttonImageX + buttonImageWidth:
                        if y > buttonImageY(1) and y < buttonImageY(1) + buttonImageHeight:
                            # Play

                            total_hits = 0
                            least = 0
                            most = 0
                            best = 100000000
                            ended = False
                            started = True
                            play = False
                            holeCount = 0

                            started = True
                        elif y > buttonImageY(2) and y < buttonImageY(2) + buttonImageHeight:
                            # Exit
                            running = False

            screen.blit(starter_img, (0, 0))
            if int(count / 60) % 2 == 0:
                screen.blit(logos[0], (logoX, logoY))

            else:
                screen.blit(logos[1], (logoX, logoY))

            screen.blit(play_img, (buttonImageX, buttonImageY(1)))
            screen.blit(exit_img, (buttonImageX, buttonImageY(2)))

            pygame.display.flip()

            count += 1

            clock.tick(FPS)
        
        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(BLACK)

            font1 = pygame.font.Font('freesansbold.ttf', 16)
            font2 = pygame.font.Font('freesansbold.ttf', 30)

            text = font2.render("Game Complete", True, WHITE)
            textRect = text.get_rect()
            textRect.center = ((SCREEN_WIDTH - 300) / 2, 200)

            text2 = font.render("Total Hits: " + str(total_hits), True, WHITE)
            textRect2 = text2.get_rect()
            textRect2.center = ((SCREEN_WIDTH - 200) / 2, 250)


            text3 = None
            if beaten:
                text3 = font.render("Best: " + str(best), True, GREEN)
            else:
                text3 = font.render("Best: " + str(best), True, WHITE)
            
            textRect3 = text3.get_rect()
            textRect3.center = ((SCREEN_WIDTH - 200) / 2, 300)
    

            text4 = font.render("Least Hits in Round: " + str(least), True, WHITE)
            textRect4 = text4.get_rect()
            textRect4.center = ((SCREEN_WIDTH - 200) / 2, 400)

            text5 = font.render("Most Hits in Round: " + str(most), True, WHITE)
            textRect5 = text5.get_rect()
            textRect5.center = ((SCREEN_WIDTH - 200) / 2, 450)

            screen.blit(text, textRect)
            screen.blit(text2, textRect2)
            screen.blit(text3, textRect3)
            screen.blit(text4, textRect4)
            screen.blit(text5, textRect5)

            pygame.display.flip()

            count += 1

            clock.tick(FPS)

            pygame.time.wait(6000)

            ended = False
        

pygame.quit()
sys.exit()
