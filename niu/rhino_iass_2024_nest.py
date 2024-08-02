#! python3

import rhinoscriptsyntax as rs
import compas
import compas_rhino.objects
import compas_rhino.conversions
from compas.geometry import Polyline
from compas.datastructures import Mesh

def get_all_child_layers(parent_layer):
    """
    Recursively find all child layers of the given parent layer.
    
    Parameters:
    parent_layer (str): The name of the parent layer.
    
    Returns:
    list: A list of all child layer names.
    """
    child_layers = rs.LayerChildren(parent_layer)
    all_child_layers = []
    
    if child_layers:
        for child in child_layers:
            all_child_layers.append(child)
            all_child_layers.extend(get_all_child_layers(child))
    
    return all_child_layers

parent_layer = "units"
child_layers = get_all_child_layers(parent_layer)

# Get objects from the parent_layer, namely polylines and meshes.
# All objects are sorted based on z coordinate.

polylines_lists = []
meshes_lists = []
for layer in child_layers:
    guids_polylines = compas_rhino.objects.get_polylines(layer)
    guids_meshes = compas_rhino.objects.get_meshes(layer)

    polylines = []
    polylines_z_coord = []
    for guid in guids_polylines:
        curve = compas_rhino.conversions.curveobject_to_compas(guid)
        polyline = curve.to_polyline()
        polylines.append(polyline)
        polylines_z_coord.append(polyline[0][2])

    paired_polylines = list(zip(polylines, polylines_z_coord))
    sorted_paired_polylines = sorted(paired_polylines, key=lambda x: x[1])
    polylines = [polyline for polyline, z in sorted_paired_polylines]
    polylines_lists.append(polylines)

    meshes = []
    meshes_z_coord = []

    for guid in guids_meshes:
        mesh = compas_rhino.conversions.meshobject_to_compas(guid)
        meshes.append(mesh)
        meshes_z_coord.append(mesh.vertex_point(0)[2])
          

    paired_meshes = list(zip(meshes, meshes_z_coord))
    print(meshes, meshes_z_coord)  
    sorted_paired_meshes = sorted(paired_meshes, key=lambda x: x[1])
    meshes = [mesh for mesh, z in sorted_paired_meshes]

    meshes_lists.append(meshes)

# Serialize these objects to json
session = {'polylines_lists': polylines_lists, 'meshes_lists': meshes_lists}
compas.json_dump(session, 'C:/brg/2_code/IASS2024_workshop_preparation/data/session.json')