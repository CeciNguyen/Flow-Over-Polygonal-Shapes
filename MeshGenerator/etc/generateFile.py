
import datetime


def foamText():
    return """
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
                   
convertToMeters 1;\n
"""

def writeBoundary(name, type, faces):
        boundary_string = f"""\t{name}
\t{{
\t\ttype {type};
\t\tfaces
\t\t(
"""
        for face in faces:
            fs = " ".join(["{:3s}".format(str(i)) for i in face])
            boundary_string += f"\t\t\t({fs})\n"
        boundary_string = boundary_string[:-1]
        boundary_string += "\n\t\t);\n\t}\n\n"
        return boundary_string

def WriteToFile(sides, diameter, foreground, wake, width, height, resolution, vertices, blocks, inlet, outlet, insideFaces, top, bottom, outside):
    with open('blockMeshDict', 'w') as file:
            today = datetime.datetime.now()
            file.write(f"// File generated on {today.strftime('%m-%d-%Y')}\n\n")
            file.write(f"// # Sides: {sides}\n")
            file.write(f"// Diameter: {diameter}\n")
            file.write(f"// Foreground: {foreground}\n")
            file.write(f"// Wake: {wake}\n")
            file.write(f"// Width: {width}\n")
            file.write(f"// Height: {height}\n")
            file.write(f"// Resolution: {resolution}\n")
            file.write(foamText())
            file.write("vertices\n(\n")
            for i,point in enumerate(vertices):
                v_string = "( {:19s} {:19s} {:5s} ) // {:3}".format(str(point[0]), str(point[1]), str(point[2]), str(i))
                file.write(f"\t\t {v_string}\n")
            file.write(");\n\n")
            file.write("blocks\n(\n")
            for s,block in enumerate(blocks):
                point_indices = " ".join(["{:3s}".format(str(i)) for i in block])
                file.write(f"\t\thex ({point_indices}) ({resolution} {resolution} 1) simpleGrading (1 1 1) // {s}\n")
            file.write(");\n\n")
            file.write("edges\n(\n")
            file.write(");\n\n")
            file.write("boundary\n(\n")
            inlet_string = writeBoundary("inlet", "patch", inlet)
            file.write(inlet_string)
            outlet_string = writeBoundary("outlet", "patch", outlet)
            file.write(outlet_string)
            polygon_string = writeBoundary("polygon", "wall", insideFaces)
            file.write(polygon_string)
            top_string = writeBoundary("top", "symmetryPlane", top)
            file.write(top_string)
            bottom_string = writeBoundary("bottom", "symmetryPlane", bottom)
            file.write(bottom_string)
            outside_string = writeBoundary("outside", "patch", outside)
            file.write(outside_string)
            file.write(");\n\n")
            file.write("mergePatchPairs\n(\n")
            file.write(");\n\n")