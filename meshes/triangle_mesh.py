from shapely import geometry
import trimesh

p1 = geometry.Point(0, 0)
p2 = geometry.Point(4, 0)
p3 = geometry.Point(2, 3.4641016151378)

points = [p1, p2, p3]

triangle = geometry.Polygon([[p.x, p.y] for p in points])

mesh = trimesh.creation.extrude_polygon(triangle, 0.5)

outfile = open("triangle.dae", "wb")
str = (trimesh.exchange.dae.export_collada(mesh))
print(str)
outfile.write(str)
outfile.close()
