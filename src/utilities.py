import pygame
import math

def loadImage(name, w = None, h = None):
    path = "/Users/princemaphupha/Desktop/Games/HoleInOne/assets/"
    img = pygame.image.load(str(path + name))
    if(w != None):
        img = pygame.transform.scale(img, (w, h))

    return img

def cartesian(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
