from compas_ifc.model import Model
from compas import json_load
from compas.geometry import Frame


# Load IFC file
model = Model("data/NEST_backbone_cleaned_up_units.ifc", use_occ=True)

# Load Session
session = json_load("data/session_nest_units_modified.json")
storey = model.building_storeys[4]


frame = Frame([0,0,0], [1, 0, 0], [0, 1, 0])
element = model.create(geometry=session["form_found"].scaled(1e3), frame=frame, name="nest_unit_form_found", parent=storey)

model.save("data/NEST_backbone_cleaned_up_units_modified.ifc")
model.show() # to big wont show up

