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

import math

def is_collision(circle_top_left, radius, rect_top_left, rect_width, rect_height):
    import math

def collision(cx, cy, radius, rx, ry, rw, rh):
    """
    Check if a circle collides with a rectangle.

    Args:
        cx (float): Circle's center x-coordinate.
        cy (float): Circle's center y-coordinate.
        radius (float): Circle's radius.
        rx (float): Rectangle's top-left x-coordinate.
        ry (float): Rectangle's top-left y-coordinate.
        rw (float): Rectangle's width.
        rh (float): Rectangle's height.

    Returns:
        bool: True if the circle and rectangle collide, False otherwise.
    """

    # Side
    side = 1

    # Temporary variables to set edges for testing
    testX = cx
    testY = cy

    # Which edge is closest?
    if cx < rx:
        testX = rx  # Test left edge
        side = 1
    elif cx > rx + rw:
        testX = rx + rw  # Test right edge
        side = 3

    if cy < ry:
        testY = ry  # Test top edge
        side = 2
    elif cy > ry + rh:
        testY = ry + rh  # Test bottom edge
        side = 4

    # Get distance from closest edges
    distX = cx - testX
    distY = cy - testY
    distance = math.sqrt((distX ** 2) + (distY ** 2))

    # If the distance is less than or equal to the radius, collision!
    bool = distance <= radius
    return [bool, side]


