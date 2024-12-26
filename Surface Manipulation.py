import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# Function to check if the input is a planar surface
def validate_planar_surface(surface):
    """Validates that the input is a planar surface.
    
    Args:
        surface: The input surface to validate (Rhino.Geometry.Surface).
        
    Returns:
        The validated surface if it is planar.
        
    Raises:
        ValueError: If the input is not a surface or not planar.
    """
    if not isinstance(surface, rg.Surface):
        raise ValueError("The input is not a valid surface.")
    
    if not surface.IsPlanar():
        raise ValueError("The input surface is not planar.")
    
    return surface

# Function to apply attraction
def apply_attraction(points, attraction_points, strength):
    """Applies attraction forces to deform grid points based on attractor points.
    
    Args:
        points: List of grid points to deform (list of Rhino.Geometry.Point3d).
        attraction_points: List of attractor points (list of Rhino.Geometry.Point3d).
        strength: Strength of the attraction effect (float).
        
    Returns:
        A list of deformed points (list of Rhino.Geometry.Point3d).
    """
    deformed_points = []
    
    # Loop over each point in the grid
    for point in points:
        influence = rg.Vector3d(0, 0, 0)
        total_weight = 0  # To normalize the influence
        
        # Apply attraction force from each attractor point
        for attraction_point in attraction_points:
            direction = attraction_point - point  # Vector from grid point to attractor
            distance = direction.Length
            direction.Unitize()  # Normalize the direction vector
            
            # Calculate the vertical distance (Z-axis difference) to the attractor
            z_diff = attraction_point.Z - point.Z
            
            # Weight the influence by the inverse of the distance
            weight = 1 / (distance + 1e-6)  # Avoid division by zero
            
            # Calculate the movement influenced by strength and Z difference
            movement = z_diff * weight * strength
            
            # Restrict movement to avoid overshooting the attractor
            if movement > 0:
                influence.Z += min(movement, z_diff)  # Move upwards but not beyond the attractor
            else:
                influence.Z += max(movement, z_diff)  # Move downwards but not beyond the attractor
            
            total_weight += weight  # Accumulate weight for normalization
        
        # Normalize the influence to prevent excessive deformation
        if total_weight > 0:
            influence.Z /= total_weight
        
        # Create the deformed point by adjusting the Z-coordinate
        deformed_point = rg.Point3d(point.X, point.Y, point.Z + influence.Z)
        deformed_points.append(deformed_point)
    
    return deformed_points

# Function to generate the deformed surface mesh
def generate_deformed_surface(surface, attraction_points, strength, divisions):
    """Generates a deformed surface mesh based on attraction points.
    
    Args:
        surface: The base planar surface (Rhino.Geometry.Surface).
        attraction_points: List of attractor points (list of Rhino.Geometry.Point3d).
        strength: Strength of attraction (float).
        divisions: Number of grid divisions (int).
        
    Returns:
        A deformed mesh surface (Rhino.Geometry.Mesh).
    """
    # Ensure divisions is a positive integer
    divisions = int(divisions)
    
    # Validate and ensure the surface is planar
    surface_geometry = validate_planar_surface(surface)
    
    # Get the domain of the surface (U, V parameters)
    u_domain = surface_geometry.Domain(0)
    v_domain = surface_geometry.Domain(1)
    
    # Create a grid of points on the surface
    points = []
    for i in range(divisions + 1):
        u_param = u_domain.T0 + (u_domain.T1 - u_domain.T0) * (i / divisions)
        for j in range(divisions + 1):
            v_param = v_domain.T0 + (v_domain.T1 - v_domain.T0) * (j / divisions)
            point = surface_geometry.PointAt(u_param, v_param)
            points.append(point)
    
    # Apply deformation to the grid points
    deformed_points = apply_attraction(points, attraction_points, strength)
    
    # Create a mesh to represent the deformed surface
    mesh = rg.Mesh()

    # Add deformed points as vertices to the mesh
    for point in deformed_points:
        mesh.Vertices.Add(point)
    
    # Add faces to the mesh to create a continuous surface
    for i in range(divisions):
        for j in range(divisions):
            idx1 = i * (divisions + 1) + j
            idx2 = idx1 + 1
            idx3 = (i + 1) * (divisions + 1) + j + 1
            idx4 = idx3 - 1
            
            # Create quadrilateral faces for each grid cell
            mesh.Faces.AddFace(idx1, idx2, idx3, idx4)
    
    return mesh

# Main logic for Grasshopper
planar_surface = PlanarSurface  # Input planar surface (from Grasshopper)
attraction_points = AttractionPoints  # List of attraction points (input from Grasshopper)
strength = Strength  # Strength of attraction (slider input)
divisions = Divisions  # Grid divisions (slider input)

# Ensure input types are correct and validate inputs
if not isinstance(planar_surface, rg.Surface):
    raise ValueError("The provided surface is not a valid Rhino surface.")
if not isinstance(attraction_points, list) or not all(isinstance(pt, rg.Point3d) for pt in attraction_points):
    raise ValueError("Attraction points must be a list of Rhino.Geometry.Point3d objects.")
if not isinstance(strength, (int, float)):
    raise ValueError("Strength must be a numeric value.")
if not isinstance(divisions, int) or divisions <= 0:
    raise ValueError("Divisions must be a positive integer.")

# Generate the deformed surface mesh
deformed_surface = generate_deformed_surface(planar_surface, attraction_points, strength, divisions)

# Output the deformed surface mesh to Grasshopper
DeformedSurface = deformed_surface  # The resulting deformed mesh surface
