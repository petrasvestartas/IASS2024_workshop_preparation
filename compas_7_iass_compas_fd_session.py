from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import NurbsCurve
from compas.geometry import Frame
from compas.geometry import Transformation
from compas_fd.constraints import Constraint
from compas_fd.solvers import fd_constrained_numpy
from compas_viewer import Viewer
from compas.colors import Color
from compas import json_load, json_dump
from compas.datastructures import Mesh

# Deserialize the session
session = json_load("data/session_nest_units_modified.json")

# Take one of the polygons
mesh = session["mesh"].copy()


# Set Fixed Vertices
fixed = list(mesh.vertices_where(vertex_degree=2))

# Change mesh vertices
mesh_vertices = list(mesh.vertices())
for idx, vertex in enumerate(fixed):
    if idx%2 == 0:
        point = mesh.vertex_point(vertex)
        mesh.set_vertex_point(mesh_vertices[vertex], [point[0],point[1],point[2]+5])

# Get Vertices and Edges
vertices = mesh.vertices_attributes("xyz")
edges = list(mesh.edges())



# Set Force Densities
q = []
for edge in edges:
    if mesh.is_edge_on_boundary(edge):
        q.append(10)
    else:
        q.append(1.0)

# Set Loads
loads = [[0, 0, 0.2] for _ in range(mesh.number_of_vertices())] 

# Set Constraints
constraints = [None] * mesh.number_of_vertices()


# Solve
result = fd_constrained_numpy(
    vertices=vertices,
    fixed=fixed,
    edges=edges,
    forcedensities=q,
    loads=loads,
    constraints=[]
)

# Update Mesh Vertices Position
for vertex, attr in mesh.vertices(data=True):
    attr["x"] = result.vertices[vertex, 0]
    attr["y"] = result.vertices[vertex, 1]
    attr["z"] = result.vertices[vertex, 2]

# Write mesh to session
transform = Transformation.from_frame_to_frame(Frame.worldXY(),session["lowest_polygons"][4].frame)
session["form_found"] = mesh.transformed(transform)
json_dump(session, "data/session_nest_units_modified.json")


# Visualize geometry in compas_viewer
viewer = Viewer()
viewer.scene.add(mesh)
viewer.show()