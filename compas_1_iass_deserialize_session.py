import compas
from compas_viewer import Viewer

# Load session made in Rhino8
session = compas.json_load("data/session_nest_units_by_storey.json")
nest_units_by_storey = session["nest_units_by_storey"]


# Visualize geometry in compas_viewer
viewer = Viewer()

for meshes_list in nest_units_by_storey:
    group = viewer.scene.add(compas.geometry.Frame(compas.geometry.Point(0,0,0)))
    for mesh in meshes_list:
        mesh.scale(0.001)
        viewer.scene.add(mesh, parent=group)

viewer.show()