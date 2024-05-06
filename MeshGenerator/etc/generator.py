from .generateBlocks import makeConnectorBlocks
from .generateFaces import makeConnectorFaces, makeTriangleFaces
from .generateFile import WriteToFile
from .generatePlot import generatePlot
from .generateVertices import (adjustVertices, createTriangles, createVertices,
                               makeConnectorRectangles)
from .mathFuncs import createWedgePoints, makePolygon
import numpy as np
import matplotlib.pyplot as plt


def MeshGeneration(sides, diameter, foreground, wake, width, height, resolution):

    full_length = foreground + width + wake

    polygon = makePolygon(diameter, sides)

    for i in range(len(polygon)):
        polygon[i] = (polygon[i][0] + (foreground + (width/2)), polygon[i][1] + (width/2))
    polygon.append(polygon[0])

    wedge = createWedgePoints(polygon)

    triangles = createTriangles(polygon, wedge)

    zero = (foreground + width/2, width/2)

    connectors = makeConnectorRectangles(triangles, width, full_length, zero)

    new_vertices = createVertices(connectors)

    vertices = adjustVertices(new_vertices, height)

    blocks = makeConnectorBlocks(connectors, vertices, height)

    top, bottom, outside, inlet, outlet = makeConnectorFaces(connectors, vertices, height, width, full_length)

    _, _, insideFaces = makeTriangleFaces(triangles, vertices, height)

    WriteToFile(sides, diameter, foreground, wake, width, height, resolution, vertices, blocks, inlet, outlet, insideFaces, top, bottom, outside)

    # generatePlot(vertices, blocks, height, width, full_length)

    # Make Mesh Top View
    outside = ((0,0), (full_length, 0), (full_length, width), (0, width), (0,0))
    plt.figure()
    plt.plot(*zip(*outside), 'k')
    for n,connector in enumerate(connectors):
        plt.plot(*zip(*connector), 'k')
        item = np.array(connector)
        middle = np.mean(item, axis=0)
        plt.text(middle[0], middle[1], str(n), fontsize=12, ha='center')
    plt.axis('equal')
    plt.show()

