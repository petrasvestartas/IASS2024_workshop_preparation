from compas_ifc.model import Model
from compas_viewer import Viewer
from compas_viewer.scene import Collection
from compas.geometry import Frame, Transformation
from compas import json_dump
model = Model("data/NEST_backbone_cleaned_up_units.ifc", use_occ=True)

ifc_building_elements = model.get_entities_by_type("IfcBuildingElementProxy")

lowest_polygons = []
extrusion_heights = []
lowest_polygons_on_xy = []

for element in ifc_building_elements:
    if(element.Name == "nest_unit"):
        if element.geometry:
            element.geometry.transform(element.frame.to_transformation())
            element.geometry.simplify(lineardeflection=0.01, angulardeflection=0.01) # merges coplanar faces such as triangles
            element.geometry.heal() # joints faces into a closed brep
            element.geometry.scale(0.001)

            # Initialize variables for lowest and highest polygons
            lowest_polygon = None
            lowest_z = float('inf')
            highest_polygon = None
            highest_z = -float('inf')

            # Iterate through faces to find both lowest and highest polygons
            for face in element.geometry.faces:
                polygon = face.to_polygon()
                centroid = polygon.centroid
                if centroid.z < lowest_z:
                    lowest_z = centroid.z
                    lowest_polygon = polygon
                if centroid.z > highest_z:
                    highest_z = centroid.z
                    highest_polygon = polygon
            
            # Orient polygon to xy plane
            lowest_polygons_on_xy.append(lowest_polygon.transformed(Transformation.from_frame_to_frame(lowest_polygon.frame, Frame.worldXY())))
            lowest_polygons.append(lowest_polygon)
            extrusion_heights.append(highest_z - lowest_z)
            
            
            
            
# Save session    
session = {
    "lowest_polygons_on_xy": lowest_polygons_on_xy,
    "lowest_polygons": lowest_polygons,
    "extrusion_heights": extrusion_heights
}

json_dump(session, "data/session_nest_units_modified.json")

viewer = Viewer()
viewer.scene.add(Collection(lowest_polygons), name="Lowest Polygon")
viewer.scene.add(Collection(lowest_polygons_on_xy), name="Lowest Polygon on XY")
viewer.show()