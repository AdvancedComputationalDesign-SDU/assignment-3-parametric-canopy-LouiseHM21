# Assignment 3: Parametric Structural Canopy Documentation

## Table of Contents

- [Pseudo-Code](#pseudo-code)
- [Technical Explanation](#technical-explanation)
- [Results](#results)
- [Challenges and Solutions](#challenges-and-solutions)
- [References](#references)

---

## Pseudo-Code

### **Main Function: Generating the Canopy**

1. **Inputs**:
   - `base_surface`: The initial surface for the canopy.
   - `depth_map_control`: Control parameter for depth variation.
   - `recursion_params`: Parameters for recursive supports (`depth`, `angle`, `length_multiplier`, etc.).
   - `tessellation_strategy`: Strategy for surface tessellation (e.g., X, Y, diagonal lines).
   - `extrema_count`: Number of extrema points to generate supports.

2. **Process**:
   - **Step 1**: Generate Depth Map:
     - Modify the `base_surface` with depth variations using a control parameter.
   - **Step 2**: Find Extremum Points:
     - Identify global and local minima and maxima on the modified surface.
   - **Step 3**: Generate Recursive Supports:
     - Use extrema points to define support placements.
     - Apply recursion to create branching structures.
   - **Step 4**: Adjust Surface Height:
     - Align the surface to match support heights.
   - **Step 5**: Tessellate the Surface:
     - Divide the surface into panels using the selected tessellation strategy.
   - **Step 6**: Apply Thickness to Supports and Tessellation:
     - Pipe the generated curves for thickness.

3. **Outputs**:
   - `canopy_mesh`: The final tessellated and thickened canopy mesh.
   - `supports`: The generated recursive support structures.

### **Functions**

- **`generate_depth_map(base_surface, control_value)`**:
  - *Purpose*: Deform the input surface to introduce depth variation.
  - *Process*: Apply sine or noise functions to create surface deformation.

- **`find_all_extrema_points(mesh)`**:
  - *Purpose*: Identify extrema points on the mesh.
  - *Process*: Loop through vertices, compare Z-coordinates, and find minima/maxima.

- **`generate_recursive_supports(start_point, params, depth)`**:
  - *Purpose*: Create branching structures recursively.
  - *Process*: Draw branches using recursion and reduce their size and angle at each step.

- **`tessellate_surface(surface, strategy)`**:
  - *Purpose*: Tessellate the surface based on the chosen strategy.
  - *Process*: Divide the surface into panels aligned with the support structure.

- **`Mesh Pipe`**:
  - *Purpose*: Apply thickness to curves for a solid structure.
  - *Process*: Pipe curves generated from tessellation and supports.

### **Workflow Diagram**

   ![Grasshopper script](images/Grasshopper_Script.png)

---

## Technical Explanation

### **Depth Map Generation**
- **Surface Deformation**:
  - The base surface is divided into a grid of control points.
  - Each grid point is displaced vertically (Z-axis) based on proximity to attractors.
  - Attractors influence points with a strength parameter and inverse-distance weighting.

- **Mathematical Functions**:
  - Attractor influence: 
    $$
    weight = \frac{1}{{distance} + \epsilon}
    $$
  - Vertical displacement: 
    $$
    movement = {z_{diff}} \times {weight} \times {strength}
    $$

- **Control Parameters**:
  - `Strength`: Intensity of deformation.
  - `Divisions`: Grid resolution.
  - `Attractor Points`: Placement and number define deformation regions.

### **Surface Tessellation**
- **Strategies**:
  - Horizontal, vertical, and diagonal tessellation lines projected onto the mesh.
  - Non-uniform tessellation achieved through sine-modulated lines.

- **Contributions to Design**:
  - Ensures alignment with the organic surface shape.
  - Enhances visual interest and structural functionality.

### **Recursive Supports Generation**
- **Recursion for Branching**:
  - Each branch spawns smaller branches with reduced length and angle.
  - Recursion stops when depth reaches zero.

- **Control Parameters**:
  - `Depth`: Number of recursion levels.
  - `Angle`: Determines branch spread and tilt.
  - `Length Multiplier`: Reduces branch size with each step.
  - `Branches`: Number of branches per node.
  - `Randomness`: Adds variation to branching angles.

---

## Results

### **Base Surface Variations**

1. **Variation 1**

   ![Base Surface 1](images/Base_Surface_1.jpg)
   ![Depth map 1](images/Depth_Map_1.jpg)
   ![Canopy 1](images/Final_Structure_1.jpg)

   - **Parameters**:
     - `Strength`: [1.0]

2. **Variation 2**

   ![Base Surface 2](images/Base_Surface_2.jpg)
   ![Depth map 2](images/Depth_Map_2.jpg)
   ![Canopy 2](images/Final_Structure_2.jpg)

   - **Parameters**:
     - `Strength`: [2.0]

3. **Variation 3**

   ![Base Surface 3](images/Base_Surface_3.jpg)
   ![Depth map 3](images/Depth_Map_3.jpg)
   ![Canopy 3](images/Final_Structure_3.jpg)

   - **Parameters**:
     - `Strength`: [1.5]

### **Tessellation Variations**

1. **Variation 1**

   ![Tessellation 1](images/Tessellation_Curves_1.jpg)

   - **Parameters**:
     - `Resolution`: [44]
     - `Frequency`: [50]
     - `Amplitude`: [20]

2. **Variation 2**

   ![Tessellation 2](images/Tessellation_Curves_2.jpg)

   - **Parameters**:
     - `Resolution`: [60]
     - `Frequency`: [42]
     - `Amplitude`: [40]

3. **Variation 3**

   ![Tessellation 3](images/Tessellation_Curves_3.jpg)

   - **Parameters**:
     - `Resolution`: [32]
     - `Frequency`: [43]
     - `Amplitude`: [4]

### **Recursive Supports Variations**

1. **Variation 1**

   ![Supports 1](images/Supports_1.jpg)

   - **Parameters**:
     - `Length_0`: [10.0]
     - `Length_Multiplier`: [1.0]
     - `Depth`: [3]
     - `Angle`: [24]
     - `Randomness`: [TRUE]
     - `Random_Offset`: [30.0]

2. **Variation 2**

   ![Supports 2](images/Supports_2.jpg)

   - **Parameters**:
     - `Length_0`: [5.0]
     - `Length_Multiplier`: [0.90]
     - `Depth`: [5]
     - `Angle`: [16]
     - `Randomness`: [FALSE]

3. **Variation 3**

   ![Supports 3](images/Supports_3.jpg)

   - **Parameters**:
     - `Length_0`: [8.0]
     - `Length_Multiplier`: [0.90]
     - `Depth`: [4]
     - `Angle`: [20]
     - `Randomness`: [TRUE]
     - `Random_Offset`: [75.0]

---

## Challenges and Solutions

### **Challenge 1: Generating Non-Planar Voronoi Structures**
- **Problem**: Difficulty in generating non-planar Voronoi patterns.
- **Solution**: Switched to a tessellation approach for better adaptability to non-planar surfaces.

### **Challenge 2: Debugging Recursive Structures**
- **Problem**: Errors in recursive functions for supports.
- **Solution**: Utilized structured testing and ChatGPT assistance to debug and refine the recursion logic.

### **Challenge 3: Complex Surface Modifications**
- **Problem**: Aligning tessellation with deformed surfaces.
- **Solution**: Adjusted control parameters and used projection methods to fit tessellation onto the modified surface.

---

## References

- **NumPy Documentation**: [https://numpy.org/doc/]  
  *(Used for numerical computations in grid and mesh manipulation.)*

- **Rhino.Python Guides**: [https://developer.rhino3d.com/guides/rhinopython/]  
  *(Provided guidance on automating Rhino for canopy generation.)*

- **RhinoScriptSyntax Documentation**: [https://developer.rhino3d.com/api/RhinoScriptSyntax/]  
  *(Used for scripting geometric transformations and tessellation within Rhino.)*

- **Matplotlib Documentation**: [https://matplotlib.org/stable/index.html]  
  *(Helped visualize support structures and depth maps.)*

- **Shapely Library**: [https://shapely.readthedocs.io/en/stable/manual.html]  
  *(Enabled precise geometric operations like recursive branching and transformations.)*
