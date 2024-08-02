from compas_ifc.model import Model
from compas_occ.brep import OCCBrep
from compas_viewer import Viewer
from compas_viewer.scene import Collection
from compas import json_load
from compas.geometry import Frame
from compas.geometry import Box
from compas.datastructures import Mesh
from compas.geometry import Sphere
from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import Polygon
from compas.geometry import bounding_box
from compas.geometry import distance_point_point_sqrd
from compas.geometry import earclip_polygon
import compas

# Load IFC file
model = Model("data/NEST_backbone_cleaned_up.ifc", use_occ=True)
session = json_load("data/session_nest_units_by_storey.json")
nest_units_by_storey = session["nest_units_by_storey"]

for i in range(len(nest_units_by_storey)):
    storey = model.building_storeys[i+2]
    for mesh in nest_units_by_storey[i]:
        frame = Frame([0,0,0], [1, 0, 0], [0, 1, 0])
        brep = OCCBrep.from_mesh(mesh)
        mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
        box  = Box(5000,5000,5000)

        element = model.create(geometry=box, frame=frame, Name="nest_unit", parent=storey)
    
# model.show()
model.save("data/NEST_backbone_cleaned_up_units.ifc")

