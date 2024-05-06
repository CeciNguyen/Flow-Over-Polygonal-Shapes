import matplotlib.pyplot as plt


def generatePlot(vertices, blocks, height, width, full_length):
    plt.figure()
    ax = plt.axes(projection='3d')
    for i,v in enumerate(vertices):
        ax.text(*v, s=f'{i}', color='black')
    for b in blocks:
        ax.plot(*zip(*[vertices[i] for i in b]))
    ax.set_box_aspect([full_length, width, height])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xticks([0, full_length/2, full_length])
    ax.set_yticks([0, width/2, width])
    ax.set_zticks([-height/2, 0, height/2])