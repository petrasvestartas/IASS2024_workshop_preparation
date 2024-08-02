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


# model = Model.template(storey_count=1)
#storey =model.create("IfcBuildingStorey", parent=building, Name=f"Default Storey {j+1}")
storey = model.building_storeys[0]
element_proxy = model.create("IfcBuildingElementProxy", frame=Frame([0, 0, 0]), Name="units", parent=storey)

# Load session made in Rhino8
session = json_load("data/session.json")
polylines_lists = session["polylines_lists"]
meshes_lists = session["meshes_lists"]

# Add elements to IFC model

for i in range(len(polylines_lists)):

    # find bottom left corner of the first polyline
    aabb = bounding_box(polylines_lists[i][0])
    bottom_left = aabb[0]
    
    # find closest point to the bottom left corner
    closest_point = polylines_lists[i][0][0]
    distance = distance_point_point_sqrd(bottom_left, closest_point)
    for point in polylines_lists[i][0]:
        if distance_point_point_sqrd(bottom_left, point) < distance:
            closest_point = point
            distance = distance_point_point_sqrd(bottom_left, point)
        
    # frame is the bottom outline most bottom left corner    
    frame = Frame(closest_point, [1, 0, 0], [0, 1, 0])
    frame = Frame([0,0,0], [1, 0, 0], [0, 1, 0])
    
    # add elements to the model
    # element_base = model.create(geometry=meshes_lists[i][0], frame=frame, Name="unit_"+str(i), parent=storey)
    
    # polygon0 = Polygon(points=polylines_lists[i][0].points[:-1])
    # polygon1 = Polygon(points=polylines_lists[i][1].points[:-1])
    
    # mesh0 = Mesh.from_vertices_and_faces(polygon0.points, earclip_polygon(polygon0))
    # mesh1 = Mesh.from_vertices_and_faces(polygon1.points, earclip_polygon(polygon1))
    # element0 = model.create(geometry=mesh0, frame=frame, Name="unit_bottom_polyline", parent=storey)
    # element1 = model.create(geometry=mesh1, frame=frame, Name="unit_top_polyline", parent=storey)   
    element2 = model.create(geometry=meshes_lists[i][0], frame=frame, Name="unit_base_mesh", parent=storey)
    # element3 = model.create(geometry=meshes_lists[i][1], frame=frame, Name="unit_volume_mesh", parent=storey)
    
    # element_polylin0 = model.create("IfcPolyline", geometry=polylines_lists[i][0], frame=frame, Name="unit_bottom_polyline", parent=storey)
    
    # box = Box.from_width_height_depth(5000, 5000, 500)
    # element3 = model.create(geometry=box, frame=frame, Name="unit_volume_mesh", parent=storey)
        
    

    
    # element3 = model.create("IfcRoof", geometry=mesh, frame=Frame([0, 0, 5000]), Name="Roof", parent=storey)
    # element2 = model.create(geometry=sphere, frame=Frame([0, 5000, 0]), Name="Sphere", parent=storey)
            
    
    # viewer.scene.add([geometry], name="unit_" + str(i), hide_coplanaredges=True, opacity=0.5, facecolor=(255, 0, 0))

# box = Box.from_width_height_depth(5000, 5000, 50)
# sphere = Sphere(2000)
# mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
# mesh.scale(1000)

# storey = model.building_storeys[0]

# element1 = model.create("IfcWall", geometry=box, frame=Frame([0, 0, 0]), Name="Wall", )
# element3 = model.create("IfcRoof", geometry=mesh, frame=Frame([0, 0, 5000]), Name="Roof", parent=storey)
# element2 = model.create(geometry=sphere, frame=Frame([0, 5000, 0]), Name="Sphere", parent=storey)


model.show()
model.save("data/NEST_backbone_cleaned_up_units.ifc")
