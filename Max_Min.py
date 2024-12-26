import Rhino.Geometry as rg

def find_all_extrema_points(mesh):
    """
    Finds global and local minima and maxima points on a 3D mesh surface based on the Z-coordinate.

    :param mesh: A 3D mesh (Rhino.Geometry.Mesh)
    :return: A list of all extrema points (global and local min/max) as Point3d objects.
    """
    if not isinstance(mesh, rg.Mesh):
        raise ValueError("Input must be a Rhino.Geometry.Mesh object.")
    
    if not mesh.IsValid:
        raise ValueError("The mesh is invalid.")
    
    # Get all vertices of the mesh
    vertices = mesh.Vertices
    topology = mesh.TopologyVertices  # Use topology to get vertex neighbors
    
    # Initialize variables to store global and local min/max points
    global_min_z = float('inf')
    global_max_z = float('-inf')
    global_min_points = []
    global_max_points = []
    local_min_points = []
    local_max_points = []

    # Iterate through all vertices
    for i in range(vertices.Count):
        vertex = vertices[i]
        z = vertex.Z

        # Update global minimum points
        if z < global_min_z:
            global_min_z = z
            global_min_points = [vertex]  # Reset to new global minimum
        elif z == global_min_z:
            global_min_points.append(vertex)  # Add to list if Z matches global minimum

        # Update global maximum points
        if z > global_max_z:
            global_max_z = z
            global_max_points = [vertex]  # Reset to new global maximum
        elif z == global_max_z:
            global_max_points.append(vertex)  # Add to list if Z matches global maximum

        # Check neighbors for local min/max
        neighbors = topology.ConnectedTopologyVertices(i)
        is_local_min = True
        is_local_max = True

        for neighbor_index in neighbors:
            neighbor_vertex = vertices[neighbor_index]
            neighbor_z = neighbor_vertex.Z

            if z >= neighbor_z:
                is_local_min = False
            if z <= neighbor_z:
                is_local_max = False

            # Break early if not a local min/max
            if not is_local_min and not is_local_max:
                break

        # Add to local min/max lists if criteria are met
        if is_local_min:
            local_min_points.append(vertex)
        if is_local_max:
            local_max_points.append(vertex)

    # Combine all points into a single list of Point3d objects
    all_points = global_min_points + global_max_points + local_min_points + local_max_points

    return all_points

# Input from Grasshopper
mesh_surface = Mesh  # Input mesh surface (Rhino.Geometry.Mesh)

# Ensure the input is valid
if mesh_surface is None or not mesh_surface.IsValid:
    raise ValueError("Invalid mesh input.")

# Find all extrema points
extrema_points = find_all_extrema_points(mesh_surface)

# Outputs to Grasshopper
ExtremaPoints = extrema_points  # List of Point3d objects
