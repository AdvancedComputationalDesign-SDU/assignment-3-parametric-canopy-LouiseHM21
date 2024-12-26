import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# Function to check if the input is a planar surface
def validate_planar_surface(surface):
    # Ensure the surface is planar
    if not isinstance(surface, rg.Surface):
        raise ValueError("The input is not a valid surface.")
    
    if not surface.IsPlanar():
        raise ValueError("The input surface is not planar.")
    
    return surface

# Function to apply attraction
def apply_attraction(points, attraction_points, strength):
    deformed_points = []
    
    # Loop over each point in the grid
    for point in points:
        influence = rg.Vector3d(0, 0, 0)
        total_weight = 0  # To normalize the influence
        
        # Apply attraction force from each attraction point
        for attraction_point in attraction_points:
            direction = attraction_point - point
            distance = direction.Length
            direction.Unitize()  # Normalize the direction vector
            
            # Calculate the distance moved in Z direction
            z_diff = attraction_point.Z - point.Z  # The vertical distance to the attractor point
            
            # Weight the influence by the distance, but move only towards the attractor (never beyond)
            weight = 1 / (distance + 1e-6)  # Avoid division by zero, keep the weight proportional to distance
            
            # Apply strength factor directly to the Z difference
            movement = z_diff * weight * strength  # Apply movement in Z direction, influenced by strength
            
            # Prevent moving past the attraction point
            if movement > 0:
                # Only move upwards (towards the attractor)
                influence.Z += min(movement, z_diff)
            else:
                # Only move downwards (away from the attractor)
                influence.Z += max(movement, z_diff)
            
            total_weight += weight
        
        # Normalize the influence to avoid over-amplification
        if total_weight > 0:
            influence.Z /= total_weight
        
        # Deform the point (move towards the attractor point in Z)
        deformed_point = rg.Point3d(point.X, point.Y, point.Z + influence.Z)
        deformed_points.append(deformed_point)
    
    return deformed_points

# Function to generate the deformed surface mesh
def generate_deformed_surface(surface, attraction_points, strength, divisions):
    # Ensure divisions is an integer
    divisions = int(divisions)
    
    # Validate and coerce the surface to planar
    surface_geometry = validate_planar_surface(surface)
    
    # Get the domain for the surface (U, V)
    u_domain = surface_geometry.Domain(0)
    v_domain = surface_geometry.Domain(1)
    
    # Create a list of points on the surface (grid points)
    points = []
    for i in range(divisions + 1):
        u_param = u_domain.T0 + (u_domain.T1 - u_domain.T0) * (i / divisions)
        for j in range(divisions + 1):
            v_param = v_domain.T0 + (v_domain.T1 - v_domain.T0) * (j / divisions)
            point = surface_geometry.PointAt(u_param, v_param)
            points.append(point)
    
    # Apply deformation based on attraction forces
    deformed_points = apply_attraction(points, attraction_points, strength)
    
    # Create a mesh and add deformed points
    mesh = rg.Mesh()

    # Add vertices (deformed points)
    for point in deformed_points:
        mesh.Vertices.Add(point)
    
    # Add faces based on the deformed grid
    for i in range(divisions):
        for j in range(divisions):
            idx1 = i * (divisions + 1) + j
            idx2 = idx1 + 1
            idx3 = (i + 1) * (divisions + 1) + j + 1
            idx4 = idx3 - 1
            
            # Add quadrilateral faces
            mesh.Faces.AddFace(idx1, idx2, idx3, idx4)
    
    return mesh

# Main logic for Grasshopper
planar_surface = PlanarSurface  # Input planar surface (from Grasshopper)
attraction_points = AttractionPoints  # List of attraction points (input from Grasshopper)
strength = Strength  # Strength of attraction (slider input)
divisions = Divisions  # Grid divisions (slider input)

# Ensure input types are correct
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