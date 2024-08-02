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

nest_units_by_storey = []
for layer in child_layers:
    guids_meshes = compas_rhino.objects.get_meshes(layer)

    meshes = []

    for guid in guids_meshes:
        mesh = compas_rhino.conversions.meshobject_to_compas(guid)
        meshes.append(mesh)
          
    nest_units_by_storey.append(meshes)

# Serialize these objects to json
session = {'nest_units_by_storey': nest_units_by_storey}
compas.json_dump(session, 'C:/brg/2_code/IASS2024_workshop_preparation/data/session_nest_units_by_storey.json')