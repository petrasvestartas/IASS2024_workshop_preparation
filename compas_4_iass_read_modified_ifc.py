from compas_ifc.model import Model
from compas_occ.brep import OCCBrep
from compas_viewer import Viewer
from compas_viewer.scene import Collection
from compas import json_load
model = Model("data/NEST_backbone_cleaned_up_units.ifc", use_occ=True)

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
viewer.show()