import compas
from compas_viewer import Viewer

# Load session made in Rhino8
session = compas.json_load("data/session.json")
meshes_lists = session["meshes_lists"]
nest_units_by_storey= [
    [meshes_lists[0][1]],
    [meshes_lists[1][0], meshes_lists[2][0], meshes_lists[3][1]],
    [meshes_lists[4][1], meshes_lists[5][1], meshes_lists[6][1]],
]


# Visualize geometry in compas_viewer
viewer = Viewer()

for nest_units in nest_units_by_storey:
    for mesh in nest_units:
        viewer.scene.add(mesh.scaled(0.001))

viewer.show()

# Serialize these objects to json
session = {'nest_units_by_storey': nest_units_by_storey}
compas.json_dump(session, 'data/session_nest_units_by_storey.json')