import Rhino.Geometry as rg

def find_all_extrema_points(mesh):
    """
    Finds global and local minima and maxima points on a 3D mesh surface based on the Z-coordinate.

    :param mesh: A 3D mesh (Rhino.Geometry.Mesh)
    :return: A list of all extrema points (global and local min/max) as Point3d objects.
    """
    # Validate the input mesh
    if not isinstance(mesh, rg.Mesh):
        raise ValueError("Input must be a Rhino.Geometry.Mesh object.")
    
    if not mesh.IsValid:
        raise ValueError("The mesh is invalid.")
    
    # Extract vertices and topology information from the mesh
    vertices = mesh.Vertices  # List of mesh vertices
    topology = mesh.TopologyVertices  # Topology to get vertex neighbors
    
    # Initialize variables for global and local extrema
    global_min_z = float('inf')  # Start with the highest possible value for global minimum
    global_max_z = float('-inf')  # Start with the lowest possible value for global maximum
    global_min_points = []  # List of vertices at global minimum
    global_max_points = []  # List of vertices at global maximum
    local_min_points = []  # List of vertices at local minima
    local_max_points = []  # List of vertices at local maxima

    # Iterate through each vertex in the mesh
    for i in range(vertices.Count):
        vertex = vertices[i]  # Current vertex
        z = vertex.Z  # Z-coordinate of the vertex

        # Update global minimum
        if z < global_min_z:
            global_min_z = z
            global_min_points = [vertex]  # Reset list for new global minimum
        elif z == global_min_z:
            global_min_points.append(vertex)  # Add to the list if Z matches global minimum

        # Update global maximum
        if z > global_max_z:
            global_max_z = z
            global_max_points = [vertex]  # Reset list for new global maximum
        elif z == global_max_z:
            global_max_points.append(vertex)  # Add to the list if Z matches global maximum

        # Check if the vertex is a local minimum or maximum
        neighbors = topology.ConnectedTopologyVertices(i)  # Get indices of neighboring vertices
        is_local_min = True  # Assume it is a local minimum
        is_local_max = True  # Assume it is a local maximum

        for neighbor_index in neighbors:
            neighbor_vertex = vertices[neighbor_index]  # Neighboring vertex
            neighbor_z = neighbor_vertex.Z  # Z-coordinate of the neighbor

            # Determine if the current vertex is not a local min/max
            if z >= neighbor_z:
                is_local_min = False
            if z <= neighbor_z:
                is_local_max = False

            # Exit early if the vertex is neither a local min nor max
            if not is_local_min and not is_local_max:
                break

        # Add the vertex to local minima/maxima lists if conditions are met
        if is_local_min:
            local_min_points.append(vertex)
        if is_local_max:
            local_max_points.append(vertex)

    # Combine global and local extrema into a single list
    all_points = global_min_points + global_max_points + local_min_points + local_max_points

    return all_points

# Input from Grasshopper
mesh_surface = Mesh  # Input mesh surface (Rhino.Geometry.Mesh)

# Ensure the input mesh is valid
if mesh_surface is None or not mesh_surface.IsValid:
    raise ValueError("Invalid mesh input.")

# Find all extrema points on the mesh
extrema_points = find_all_extrema_points(mesh_surface)

# Outputs to Grasshopper
ExtremaPoints = extrema_points  # List of Point3d objects representing extrema points
