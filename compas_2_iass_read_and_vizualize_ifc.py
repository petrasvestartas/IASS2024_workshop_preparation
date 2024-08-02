from compas_ifc.model import Model
from compas_occ.brep import OCCBrep
from compas_viewer import Viewer
from compas_viewer.scene import Collection
from compas import json_load
model = Model("data/NEST_backbone_cleaned_up.ifc", use_occ=True)

breps = []
for element in model.building_elements:
    if element.geometry:
        element.geometry.transform(element.frame.to_transformation())
        element.geometry.simplify(lineardeflection=0.01, angulardeflection=0.01) # merges coplanar faces such as triangles
        element.geometry.heal() # joints faces into a closed brep
        element.geometry.scale(0.001)
        breps.append(element.geometry)
                
# Visualize geometry in compas_viewer
viewer = Viewer()
viewer.scene.add(Collection(breps), name="Brep")

# Load session made in Rhino8
session = json_load("data/session.json")
polylines_lists = session["polylines_lists"]
meshes_lists = session["meshes_lists"]

for i in range(len(polylines_lists)):
    geometry = []
    for polyline in polylines_lists[i]:
        polyline.scale(0.001)
        geometry.append(polyline)
    for mesh in meshes_lists[i]:
        mesh.scale(0.001)
        geometry.append(mesh)
    viewer.scene.add([geometry], name="unit_" + str(i), hide_coplanaredges=True, opacity=0.5, facecolor=(255, 0, 0))

viewer.show()