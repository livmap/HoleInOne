import pygame

def loadImage(name, w = None, h = None):
    path = "/Users/princemaphupha/Desktop/Games/HoleInOne/assets/"
    img = pygame.image.load(str(path + name))
    if(w != None):
        img = pygame.transform.scale(img, (w, h))

    return img

