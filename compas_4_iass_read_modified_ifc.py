from compas_ifc.model import Model
from compas_viewer import Viewer
from compas_viewer.scene import Collection
model = Model("data/NEST_backbone_cleaned_up_units.ifc", use_occ=True)

ifc_building_elements = model.get_entities_by_type("IfcBuildingElementProxy")
# ifc_building_elements_by_name = model.get_entities_by_type("nest_unit")
# print(ifc_building_elements_by_name)

breps = []
for element in ifc_building_elements:
    if(element.Name == "nest_unit"):
        if element.geometry:
            element.geometry.transform(element.frame.to_transformation())
            element.geometry.simplify(lineardeflection=0.01, angulardeflection=0.01) # merges coplanar faces such as triangles
            element.geometry.heal() # joints faces into a closed brep
            element.geometry.scale(0.001)
            breps.append(element.geometry)
            
# Visualize geometry in compas_viewer
# print(breps)
viewer = Viewer()
viewer.scene.add(Collection(breps), name="Brep")
viewer.show()