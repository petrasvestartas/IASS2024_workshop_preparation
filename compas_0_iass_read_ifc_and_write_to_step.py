from compas_ifc.model import Model
from compas_occ.brep import OCCBrep
from compas_viewer import Viewer

model = Model("data/NEST_backbone_cleaned_up.ifc", use_occ=True)

breps = []
counter = 0
for element in model.building_elements:
    if element.geometry:
        element.geometry.transform(element.frame.to_transformation())
        element.geometry.simplify(lineardeflection=0.01, angulardeflection=0.01) # merges coplanar faces such as triangles
        element.geometry.heal() # joints faces into a closed brep
        breps.append(element.geometry)

brep = OCCBrep.from_breps(breps)
brep.to_step("data/cleaned_up.stp")
