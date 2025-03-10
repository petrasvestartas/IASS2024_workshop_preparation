import compas
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Frame
from compas_ifc.model import Model


model = Model.template(storey_count=1, unit="m")

box = Box.from_width_height_depth(5, 5, 0.05)
sphere = Sphere(2)
mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

storey = model.building_storeys[0]

element1 = model.create("IfcWall", geometry=box, frame=Frame([0, 0, 0]), name="Wall", parent=storey)
element2 = model.create("IfcRoof", geometry=mesh, frame=Frame([0, 0, 5]), name="Roof", parent=storey)
element3 = model.create(geometry=sphere, frame=Frame([0, 5, 0]), name="Sphere", parent=storey, properties={"Custom_Pset": {"Custom_Property": "Custom Value"}})



model.print_spatial_hierarchy(max_depth=5)
model.save("temp/create_geometry.ifc")


# Load IFC file
open_model = Model("temp/create_geometry.ifc", load_geometries=True)

# open_model.show()