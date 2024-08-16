from compas_ifc.model import Model
from compas import json_load
from compas.geometry import Frame

# Load IFC file
model = Model("data/NEST_backbone_cleaned_up.ifc", use_occ=True)

# Load Session
session = json_load("data/session_nest_units_by_storey.json")
nest_units_by_storey = session["nest_units_by_storey"]

for i in range(len(nest_units_by_storey)):
    storey = model.building_storeys[i+2]
    for mesh in nest_units_by_storey[i]:
        frame = Frame([0,0,0], [1, 0, 0], [0, 1, 0])
        element = model.create(geometry=mesh, frame=frame, name="nest_unit", parent=storey)
    
model.save("data/NEST_backbone_cleaned_up_units.ifc")
model.show() # to big wont show up

