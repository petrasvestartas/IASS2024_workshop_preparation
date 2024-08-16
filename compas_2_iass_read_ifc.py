from compas_ifc.model import Model
from compas_viewer import Viewer
from compas_viewer.scene import Collection
from compas import json_load
from compas.geometry import Frame, Point
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
session = json_load("data/session_nest_units_by_storey.json")
nest_units_by_storey = session["nest_units_by_storey"]
for meshes_list in nest_units_by_storey:
    group = viewer.scene.add(Frame(Point(0,0,0)))
    for mesh in meshes_list:
        mesh.scale(0.001)
        viewer.scene.add(mesh, parent=group, opacity=0.5, facecolor=(255,0,0), hide_coplanaredges=True)

viewer.show()