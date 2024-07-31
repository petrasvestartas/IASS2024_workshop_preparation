import compas
from compas_viewer import Viewer

# Load session made in Rhino8
session = compas.json_load("data/session.json")
polylines_lists = session["polylines_lists"]
meshes_lists = session["meshes_lists"]


# Visualize geometry in compas_viewer
viewer = Viewer()
for polylines_list in polylines_lists:
    for polyline in polylines_list:
        polyline.scale(0.001)
        viewer.scene.add(polyline)

for meshes_list in meshes_lists:
    for mesh in meshes_list:
        mesh.scale(0.001)
        viewer.scene.add(mesh)

viewer.show()