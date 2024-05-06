from .generateVertices import findIndex


def makeConnectorBlocks(rects, vertices, height):
    h = height/2
    blocks = []
    for t in rects:
        p1, p2, p3, p4 = t
        po1 = (p1[0], p1[1], -h)
        po2 = (p2[0], p2[1], -h)
        po3 = (p3[0], p3[1], -h)
        po4 = (p4[0], p4[1], -h)
        po5 = (p1[0], p1[1], h)
        po6 = (p2[0], p2[1], h)
        po7 = (p3[0], p3[1], h)
        po8 = (p4[0], p4[1], h)
        i1, i2, i3, i4, i5, i6, i7, i8 = findIndex(po1, vertices), findIndex(po2, vertices), findIndex(po3, vertices), findIndex(po4, vertices), findIndex(po5, vertices), findIndex(po6, vertices), findIndex(po7, vertices), findIndex(po8, vertices)
        blocks.append([i1, i2, i3, i4, i5, i6, i7, i8])
    return blocks

def makeTriangleBlocks(triangles, vertices, height):
    h = height/2
    blocks = []
    for t in triangles:
        w1, p2, p1 = t
        po1 = (w1[0], w1[1], -h)
        po2 = (p2[0], p2[1], -h)
        po3 = (p1[0], p1[1], -h)
        po4 = (w1[0], w1[1], h)
        po5 = (p2[0], p2[1], h)
        po6 = (p1[0], p1[1], h)
        i1, i2, i3, i4, i5, i6 = findIndex(po1, vertices), findIndex(po2, vertices), findIndex(po3, vertices), findIndex(po4, vertices), findIndex(po5, vertices), findIndex(po6, vertices)
        blocks.append([i1, i2, i2, i3, i4, i5, i5, i6])
    return blocks