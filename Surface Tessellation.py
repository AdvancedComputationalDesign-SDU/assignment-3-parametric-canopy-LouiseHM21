import math
import Rhino.Geometry as rg

# Input: Mesh (Mesh)
# Output: TessellateLines (Curves)

def tessellate_mesh(mesh, resolution, frequency, amplitude):
    """Tessellates a mesh with X, Y, and diagonal lines that conform to the surface of the mesh.
    
    Args:
        mesh: Input mesh to tessellate (Rhino.Geometry.Mesh).
        resolution: Number of lines in the tessellation.
        frequency: Frequency of the sine function.
        amplitude: Amplitude of the sine function (variation in spacing).
        
    Returns:
        A list of curves forming the tessellation.
    """
    if not isinstance(mesh, rg.Mesh):  # Ensure input is a valid mesh
        return None

    # Get the bounding box of the mesh and its parameters
    bbox = mesh.GetBoundingBox(True)
    min_pt = bbox.Min
    max_pt = bbox.Max

    # Calculate the dimensions of the bounding box
    width = max_pt.X - min_pt.X
    height = max_pt.Y - min_pt.Y

    # Initialize a list to store tessellation lines
    tessellate_lines = []

    # Generate tessellation lines in the X (horizontal) direction
    for i in range(resolution + 1):
        t = i / resolution  # Normalized parameter for interpolation
        y = min_pt.Y + t * height  # Interpolated Y-coordinate
        y += math.sin(t * math.pi * frequency) * amplitude  # Add sine-based variation

        # Create a horizontal line and project it onto the mesh
        start = rg.Point3d(min_pt.X, y, 0)
        end = rg.Point3d(max_pt.X, y, 0)
        line = rg.Line(start, end).ToNurbsCurve()
        projected_line = rg.Curve.ProjectToMesh(line, mesh, rg.Vector3d(0, 0, -1), 0.01)
        if projected_line:
            tessellate_lines.append(projected_line[0])  # Store the projected curve

    # Generate tessellation lines in the Y (vertical) direction
    for i in range(resolution + 1):
        t = i / resolution  # Normalized parameter for interpolation
        x = min_pt.X + t * width  # Interpolated X-coordinate
        x += math.sin(t * math.pi * frequency) * amplitude  # Add sine-based variation

        # Create a vertical line and project it onto the mesh
        start = rg.Point3d(x, min_pt.Y, 0)
        end = rg.Point3d(x, max_pt.Y, 0)
        line = rg.Line(start, end).ToNurbsCurve()
        projected_line = rg.Curve.ProjectToMesh(line, mesh, rg.Vector3d(0, 0, -1), 0.01)
        if projected_line:
            tessellate_lines.append(projected_line[0])  # Store the projected curve

    # Generate diagonal tessellation lines across the mesh
    for i in range(resolution + 1):
        t = i / resolution  # Normalized parameter for interpolation

        # Diagonal line from bottom-left to top-right
        start = rg.Point3d(min_pt.X, min_pt.Y + t * height, 0)
        end = rg.Point3d(max_pt.X, min_pt.Y + t * height - width, 0)
        diagonal1 = rg.Line(start, end).ToNurbsCurve()
        projected_diagonal1 = rg.Curve.ProjectToMesh(diagonal1, mesh, rg.Vector3d(0, 0, -1), 0.01)
        if projected_diagonal1:
            tessellate_lines.append(projected_diagonal1[0])  # Store the projected curve

        # Diagonal line from bottom-right to top-left
        start = rg.Point3d(max_pt.X, min_pt.Y + t * height, 0)
        end = rg.Point3d(min_pt.X, min_pt.Y + t * height + width, 0)
        diagonal2 = rg.Line(start, end).ToNurbsCurve()
        projected_diagonal2 = rg.Curve.ProjectToMesh(diagonal2, mesh, rg.Vector3d(0, 0, -1), 0.01)
        if projected_diagonal2:
            tessellate_lines.append(projected_diagonal2[0])  # Store the projected curve

    return tessellate_lines  # Return all tessellation lines

# Grasshopper Input: Mesh (Mesh)
Mesh = Mesh  # Connect a mesh object from Grasshopper

# Grasshopper Output: TessellateLines (Curves)

# Parameters
resolution = Resolution  # Number of tessellation lines
frequency = Frequency  # Frequency of sine wave modulation
amplitude = Amplitude  # Amplitude of sine wave modulation

# Generate tessellation lines on the mesh
TessellateLines = tessellate_mesh(Mesh, resolution, frequency, amplitude)
