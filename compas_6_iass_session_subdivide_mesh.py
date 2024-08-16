
from compas_viewer import Viewer
from compas.geometry import earclip_polygon
from compas.datastructures import Mesh
from compas import json_load, json_dump

# Deserialize the session
session = json_load("data/session_nest_units_modified.json")

# Take one of the polygons
polygon = session["lowest_polygons_on_xy"][4]

# Create a mesh from the polygon
mesh = Mesh.from_vertices_and_faces(polygon.points, earclip_polygon(polygon))
mesh = Mesh.from_polygons([polygon])
mesh = mesh.subdivided(scheme = "catmullclark", k=3, fixed = mesh.vertices_on_boundaries()[0])

# Write mesh to session
session["mesh"] = mesh
json_dump(session, "data/session_nest_units_modified.json")

# Visualize geometry in compas_viewer
viewer = Viewer()
viewer.scene.add(mesh)
viewer.show()