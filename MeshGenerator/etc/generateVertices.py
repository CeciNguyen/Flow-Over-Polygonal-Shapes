from .mathFuncs import (isInBlocks, isSamePoint, isSamePoint3D, onPoly,
                        tolerance)


def createTriangles(poly, wedge):
    triangles = []
    wi = 0
    pi = 0
    while pi < len(poly) - 1:
        if not abs(poly[pi+1][1] - poly[pi][1]) < tolerance:
            p1 = poly[pi]
            p2 = wedge[wi]
            p3 = poly[pi+1]
            wi += 1
        pi += 1
        triangles.append((p2, p3, p1))
    return triangles

def createVertices(triangles):
    vertices = []
    for v in triangles:
        for p in v:
            if not onPoly(p, vertices):
                vertices.append(p)
    return vertices

def adjustVertices(vertices, height):
    bottom = []
    for i, v in enumerate(vertices):
        x, y = v
        vertices[i] = (x, y, height/2)
        bottom.append((x, y, -height/2))
    return vertices + bottom

def findIndex(p1, vertices):
    for i, v in enumerate(vertices):
        if isSamePoint3D(p1, v):
            return i
    return -1

def makeConnectorRectangles(triangles, width, length, zero):
    blocks = []
    for t in triangles:
        p1, p2, p3 = t
        xval = length if zero[0] < p1[0] else 0
        yval = width if abs(p1[1] - width) < p1[1] else 0
        point_1, point_2, point_3, point_4 = None, None, None, None
        if abs((p1[0] - zero[0])) > abs((p1[1] - zero[1])):
            pc, po = (p2, p3) if isSamePoint((p2[0], 0), (p1[0], 0)) else (p3, p2)
            x2 = pc[0]
            x3 = po[0]
            y1 = p1[1]
            y2 = pc[1]
            if xval != 0:
                point_1 = (xval, max(y1, y2))
                if isSamePoint(p2, pc):
                    point_2 = (x2, max(y1, y2))
                    point_3 = (x3, min(y1, y2))
                    point_4 = (xval, min(y1, y2))
                else:
                    point_2 = (x3, max(y1, y2))
                    point_3 = (x2, min(y1, y2))
                    point_4 = (xval, min(y1, y2))
            else:
                point_1 = (0, min(y1, y2))
                if isSamePoint(p2, pc):
                    point_2 = (x2, min(y1, y2))
                    point_3 = (x3, max(y1, y2))
                    point_4 = (0, max(y1, y2))
                else:
                    point_2 = (x3, min(y1, y2))
                    point_3 = (x2, max(y1, y2))
                    point_4 = (0, max(y1, y2))
        else:
            pc, po = (p2, p3) if isSamePoint((0, p2[1]), (0, p1[1])) else (p3, p2)
            y2 = pc[1]
            y3 = po[1]
            x1 = p1[0]
            x2 = pc[0]
            if yval != 0:
                point_1 = (min(x1, x2), yval)
                if isSamePoint(p2, pc):
                    point_2 = (min(x1, x2), y2)
                    point_3 = (max(x1, x2), y3)
                    point_4 = (max(x1, x2), yval)
                else:
                    point_2 = (min(x1, x2), y3)
                    point_3 = (max(x1, x2), y2)
                    point_4 = (max(x1, x2), yval)
            else:
                point_1 = (max(x1, x2), yval)
                if isSamePoint(p2, pc):
                    point_2 = (max(x1, x2), y2)
                    point_3 = (min(x1, x2), y3)
                    point_4 = (min(x1, x2), yval)
                else:
                    point_2 = (max(x1, x2), y3)
                    point_3 = (min(x1, x2), y2)
                    point_4 = (min(x1, x2), yval)
        newb = (point_1, point_2, point_3, point_4)
        blocks.append(newb)
                
    # Add filler rectangles

    # Front

    f_blocks = sorted([x for x in blocks if x[0][0] == 0], key=lambda x: x[0][1])
    sx = 0
    sy = 0
    newBlocks = []
    for b in f_blocks:
        if isSamePoint((sx,sy), b[0]):
            sx, sy = 0, b[3][1]
            continue
        ex, ey = b[1]
        nb = ((sx,sy), (ex,sy), (ex,ey), (sx,ey))
        if not isInBlocks(nb, newBlocks):
            newBlocks.append(nb)
        sx, sy = 0, b[3][1]
    if len(f_blocks) > 0:
        nb = ((sx,sy), (ex, sy), (ex, width), (0, width))
        if not isInBlocks(nb, newBlocks):
            newBlocks.append(nb)

    w_blocks = sorted([x for x in blocks if x[0][0] == length], key=lambda x: x[0][1])
    sx = length
    sy = 0
    for b in w_blocks:
        if isSamePoint((sx,sy), b[3]):
            sx,sy = length, b[0][1]
            continue
        ex, ey = b[2]
        nb=((sx,ey), (ex,ey), (ex,sy), (sx,sy))
        if not isInBlocks(nb, newBlocks):
            newBlocks.append(nb)
        sx, sy = length, b[0][1]
    if len(w_blocks) > 0:
        nb=((sx,width), (ex, width), (ex, sy), (sx, sy))
        if not isInBlocks(nb, newBlocks):
            newBlocks.append(nb)
    
    b_blocks = sorted([x for x in blocks if x[0][1] == 0], key=lambda x: x[0][0])
    sx = 0
    sy = 0
    for b in b_blocks:
        if isSamePoint((sx,sy), b[3]):
            sx,sy=b[0][0], 0
            continue
        ex, ey = b[2]
        nb = ((ex,sy), (ex,ey), (sx,ey), (sx,sy))
        if not isInBlocks(nb, newBlocks):
            newBlocks.append(nb)
        sx, sy = b[0][0], 0
    if len(b_blocks) > 0:
        nb=((length,sy), (length, ey), (sx, ey), (sx, sy))
        if not isInBlocks(nb, newBlocks):
            newBlocks.append(nb)

    t_blocks = sorted([x for x in blocks if x[0][1] == width], key=lambda x: x[0][0])
    sx = 0
    sy = width
    for b in t_blocks:
        if isSamePoint((sx,sy), b[0]):
            sx,sy=b[3][0], width
            continue
        ex, ey = b[1]
        nb=((sx,sy), (sx,ey), (ex,ey), (ex,sy))
        if not isInBlocks(nb, newBlocks):
            newBlocks.append(nb)
        sx, sy = b[3][0], width
    if len(t_blocks) > 0:
        nb=((sx,sy), (sx, ey), (length, ey), (length, sy))
        if not isInBlocks(nb, newBlocks):
            newBlocks.append(nb)
    blocks.extend(newBlocks)
    return blocks