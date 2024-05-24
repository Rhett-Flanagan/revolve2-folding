from shapely import geometry
import trimesh
import numpy

p1 = geometry.Point(0, 0)
p2 = geometry.Point(4, 0)
p3 = geometry.Point(2, 3.4641016151378)

points = [p1, p2, p3]

triangle = geometry.Polygon([[p.x, p.y] for p in points])

mesh = trimesh.creation.extrude_polygon(triangle, 0.5)
mesh.apply_transform(
    numpy.eye(4) /20
)

outfile = open("triangle.stl", "wb")
str = (trimesh.exchange.stl.export_stl(mesh))
print(mesh.extents)
outfile.write(str)
outfile.close()
