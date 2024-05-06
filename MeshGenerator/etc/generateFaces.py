from .generateVertices import findIndex
from .mathFuncs import findPlaneNormal


def makeTriangleFaces(triangles, vertices, height):
    h = height/2
    topFaces = []
    bottomFaces = []
    slantFaces = []
    for t in triangles:
        w1, p2, p1 = t
        po1 = (w1[0], w1[1], -h)
        po2 = (p2[0], p2[1], -h)
        po3 = (p1[0], p1[1], -h)
        po4 = (w1[0], w1[1], h)
        po5 = (p2[0], p2[1], h)
        po6 = (p1[0], p1[1], h)
        i1, i2, i3, i4, i5, i6 = findIndex(po1, vertices), findIndex(po2, vertices), findIndex(po3, vertices), findIndex(po4, vertices), findIndex(po5, vertices), findIndex(po6, vertices)
        topFaces.append([i4, i5, i5, i6])
        bottomFaces.append([i1, i2, i2, i3])
        slantFaces.append([max(i2, i3), max(i5, i6), min(i5, i6), min(i2, i3)])
    return topFaces, bottomFaces, slantFaces

def makeConnectorFaces(connectors, vertices, height, width, length):
    h = height/2
    topFaces = []
    bottomFaces = []
    outsideFaces = []
    inlet = []
    outlet = []
    for b in connectors:
        p1, p2, p3, p4 = b
        po1 = (p1[0], p1[1], -h)
        po2 = (p2[0], p2[1], -h)
        po3 = (p3[0], p3[1], -h)
        po4 = (p4[0], p4[1], -h)
        po5 = (p1[0], p1[1], h)
        po6 = (p2[0], p2[1], h)
        po7 = (p3[0], p3[1], h)
        po8 = (p4[0], p4[1], h)
        i1, i2, i3, i4, i5, i6, i7, i8 = findIndex(po1, vertices), findIndex(po2, vertices), findIndex(po3, vertices), findIndex(po4, vertices), findIndex(po5, vertices), findIndex(po6, vertices), findIndex(po7, vertices), findIndex(po8, vertices)
        topFaces.append([i5, i6, i7, i8])
        bottomFaces.append([i1, i2, i3, i4])
        pts = [po1, po2, po3, po4]
        onWall = []
        np1 = []
        np = []
        for p in pts:
            if p[0] == 0 or p[0] == length or p[1] == 0 or p[1] == width:
                onWall.append(p)
        if len(onWall) == 2 and onWall[0][0] == 0:
            a1, a2 = (onWall[0], onWall[1]) if onWall[0][1] < onWall[1][1] else (onWall[1], onWall[0])
            a3, a4 = (a1[0], a1[1], h), (a2[0], a2[1], h)
            np = [a1, a3, a4, a2]
        elif len(onWall) == 2 and onWall[0][0] == length:
            a1, a2 = (onWall[0], onWall[1]) if onWall[0][1] > onWall[1][1] else (onWall[1], onWall[0])
            a3, a4 = (a1[0], a1[1], h), (a2[0], a2[1], h)
            np = [a1, a3, a4, a2]
        elif len(onWall) == 2 and onWall[0][1] == 0:
            a1, a2 = (onWall[0], onWall[1]) if onWall[0][0] > onWall[1][0] else (onWall[1], onWall[0])
            a3, a4 = (a1[0], a1[1], h), (a2[0], a2[1], h)
            np = [a1, a3, a4, a2]
        elif len(onWall) == 2 and onWall[0][1] == width:
            a1, a2 = (onWall[0], onWall[1]) if onWall[0][0] < onWall[1][0] else (onWall[1], onWall[0])
            a3, a4 = (a1[0], a1[1], h), (a2[0], a2[1], h)
            np = [a1, a3, a4, a2]
        else: 
            for p in onWall:
                if (
                    p[0] == 0 and p[1] == 0 or
                    p[0] == 0 and p[1] == width or
                    p[0] == length and p[1] == 0 or
                    p[0] == length and p[1] == width
                ):
                    thePoint = p
                    break
            onWall.remove(thePoint)
            px, py = (onWall[0], onWall[1]) if onWall[0][0] == thePoint[0] else (onWall[1], onWall[0])
            if thePoint[0] == 0 and thePoint[1] == 0:
                np = [px, (px[0], px[1], h), (thePoint[0], thePoint[1], h), thePoint]
                np1 = [thePoint, (thePoint[0], thePoint[1], h), (py[0], py[1], h), py]
            elif thePoint[0] == 0 and thePoint[1] == width:
                np = [py, (py[0], py[1], h), (thePoint[0], thePoint[1], h), thePoint]
                np1 = [thePoint, (thePoint[0], thePoint[1], h), (px[0], px[1], h), px]
            elif thePoint[0] == length and thePoint[1] == 0:
                np = [thePoint, (thePoint[0], thePoint[1], h), (px[0], px[1], h), px]
                np1 = [py, (py[0], py[1], h), (thePoint[0], thePoint[1], h), thePoint]
            else:
                np = [thePoint, (thePoint[0], thePoint[1], h), (py[0], py[1], h), py]
                np1 = [px, (px[0], px[1], h), (thePoint[0], thePoint[1], h), thePoint]
        if len(np) == 4:
            i1, i2, i3, i4 = findIndex(np[0], vertices), findIndex(np[1], vertices), findIndex(np[2], vertices), findIndex(np[3], vertices)
            normal = findPlaneNormal(np[0], np[1], np[2])
            if normal[1] == 0:
                if np[0][0] == 0:
                    inlet.append([i1, i2, i3, i4][::-1])
                else:
                    outlet.append([i1, i2, i3, i4][::-1])
            else:
                outsideFaces.append([i1, i2, i3, i4][::-1])
        if len(np1) == 4:
            i1, i2, i3, i4 = findIndex(np1[0], vertices), findIndex(np1[1], vertices), findIndex(np1[2], vertices), findIndex(np1[3], vertices)
            normal = findPlaneNormal(np1[0], np1[1], np1[2])
            if normal[1] == 0:
                if np1[0][0] == 0:
                    inlet.append([i1, i2, i3, i4][::-1])
                else:
                    outlet.append([i1, i2, i3, i4][::-1])
            else:
                outsideFaces.append([i1, i2, i3, i4][::-1])
    return topFaces, bottomFaces, outsideFaces, inlet, outlet