import math
import Rhino.Geometry as rg
import random  # Import random module for randomness

# Base case: when the depth of the recursive function is zero, it stops running
def base_case(depth):
    return depth <= 0

# Drawing a branch and collecting points and lines
def draw_tree_branch(start_point, length, angle_xy, angle_z):
    """
    Draws a branch of the tree and returns its endpoint.

    :param start_point: The start point of the branch (Point3d)
    :param length: Length of the branch
    :param angle_xy: Angle in the X-Y plane (radians)
    :param angle_z: Angle from the Z-axis (radians)
    :return: The end point of the branch (Point3d)
    """
    # Calculate the end point of a branch in 3D
    end_point = rg.Point3d(
        start_point.X + length * math.cos(angle_xy) * math.cos(angle_z),  # X component
        start_point.Y + length * math.sin(angle_xy) * math.cos(angle_z),  # Y component
        start_point.Z + length * math.sin(angle_z)                         # Z component
    )
    
    # Create the line between start and end points
    line = rg.Line(start_point, end_point)
    lines_list.append(line)  # Collect line

    points_list.append(start_point)
    points_list.append(end_point)

    return end_point  # Return end_point for recursive use

# Recursive case
def recursive_case(start_point, length, angle_xy, angle_z, depth, max_depth, branches=3, length_multiplier=0.7, angle_offset_xy_max=math.radians(30), angle_offset_z=math.radians(15), randomize_angles=False):
    """
    Recursively generates branches of the tree.

    :param start_point: The start point of the branch (Point3d)
    :param length: Length of the branch
    :param angle_xy: Angle in the X-Y plane (radians)
    :param angle_z: Angle from the Z-axis (radians)
    :param depth: Current depth of recursion
    :param max_depth: Maximum recursion depth
    :param branches: Number of branches per node
    :param length_multiplier: Reduction factor for branch length
    :param angle_offset_xy_max: Maximum angle offset in the X-Y plane
    :param angle_offset_z: Maximum angle offset along the Z-axis
    :param randomize_angles: Boolean for adding randomness to branching angles
    """
    # Stop if base case is met
    if base_case(depth):
        return

    # Draw the branch and add points and lines
    end_point = draw_tree_branch(start_point, length, angle_xy, angle_z)

    # Recursive branching: Generate branches for each level
    for i in range(branches):
        if randomize_angles:
            # Randomly offset the angle in the X-Y plane within ±angle_offset_xy_max
            random_angle_offset = random.uniform(-angle_offset_xy_max, angle_offset_xy_max)
            new_angle_xy = angle_xy + (i - 1) * math.radians(120) + random_angle_offset
        else:
            # If no randomness, keep the angle fixed at 120 degrees between branches
            new_angle_xy = angle_xy + (i - 1) * math.radians(120)

        # Reduce branch length by the multiplier
        new_length = length * length_multiplier

        # Apply an offset for the angle along the Z-axis
        new_angle_z = angle_z + (branches - 1) * angle_offset_z / 2

        # Recursive call for each branch
        recursive_case(end_point, new_length, new_angle_xy, new_angle_z, depth - 1, max_depth, branches, length_multiplier, angle_offset_xy_max, angle_offset_z, randomize_angles)

# Inputs from Grasshopper
Start_Points = Start_Points  # List of starting points (list of Rhino.Geometry.Point3d)
max_depth = Depth  # Maximum depth (integer, connected to slider)
initial_length = Length_0  # Initial branch length (float, connected to slider)
length_multiplier = Length_Multiplier  # Length reduction factor per level (float, 0.1 to 1.0, connected to slider)
angle_z = Angle  # Angle between Z-axis and X-Y plane (degrees, connected to slider)
angle_offset_xy_max = Random_Offset  # Maximum offset in the X-Y plane (degrees, connected to slider)
randomize_angles = Randomness  # Boolean toggle for randomness (True/False)

# Convert the input angle to radians
angle_offset_z = math.radians(angle_z)

# Lists to store points and lines
points_list = []
lines_list = []

# Call the recursive function for each starting point
for start_point in Start_Points:
    recursive_case(
        start_point=start_point,  # Current starting point from Grasshopper
        length=initial_length,
        angle_xy=0,  # Initial angle for the X-Y plane
        angle_z=math.pi / 2,  # Start vertical
        depth=max_depth,
        max_depth=max_depth,
        branches=3,  # Number of branches per node
        length_multiplier=length_multiplier,
        angle_offset_xy_max=math.radians(angle_offset_xy_max),  # Convert to radians
        angle_offset_z=angle_offset_z,
        randomize_angles=randomize_angles
    )

# Outputs to Grasshopper
Lines = lines_list  # Output lines as Rhino.Geometry.Line objects
Points = list(set(points_list))  # Output unique points
