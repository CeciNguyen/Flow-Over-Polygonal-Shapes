import numpy as np

# Prevents duplicate indices from floating point errors.
tolerance = 0.0001

def makePolygon(diameter, sides):
    points = []
    for i in range(sides):
        angle = (2 * np.pi * i / sides)
        x = (diameter / 2) * np.cos(angle)
        y = (diameter / 2) * np.sin(angle)
        points.append((x, y))
    return points

def makeRectangle(length, width):
    points = [(0,0)]
    points.append((length, 0))
    points.append((length, width))
    points.append((0, width))
    return points

def checkInside(poly, point):
    x, y = point
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def onPoly(p1, item):
    for i in item:
        if isSamePoint(p1, i):
            return True
    return False

def isSamePoint(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    tol = abs(x1 - x2)
    toly = abs(y1 - y2)
    if tol < tolerance and toly < tolerance:
        return True
    return False

def isSamePoint3D(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    tol = abs(x1 - x2)
    toly = abs(y1 - y2)
    tolz = abs(z1 - z2)
    if tol < 0.0001 and toly < 0.0001 and tolz < 0.0001:
        return True
    return False

def isSameBlock(b1, b2):
    count = 0
    for i in range(len(b1)):
        for s in b2:
            if isSamePoint(b1[i], s):
                count += 1
    return count == 4

def isInBlocks(b, blocks):
    for bl in blocks:
        if isSameBlock(b, bl):
            return True
    return False

def isCorner(b, width, length):
    count = 0
    for p in list(b):
        if p[0] == 0 or p[0] == length or p[1] == 0 or p[1] == width:
            count += 1
    return count == 3

def findPlaneNormal(p1, p2, p3):
    v1 = np.array(p2) - np.array(p1)
    v2 = np.array(p3) - np.array(p1)
    normal = np.cross(v1, v2)
    for i in range(len(normal)):
        if abs(normal[i]) < 0.0001:
            normal[i] = 0
    return normal

def createWedgePoints(circle):
    points = []
    for i in range(0, len(circle) - 1):
        point = (circle[i][0], circle[i+1][1])
        point2 = (circle[i+1][0], circle[i][1])
        if not checkInside(circle, point) and not onPoly(point, circle):
            points.append(point)
        elif not onPoly(point2, circle):
            points.append(point2)
    return points