# Assignment 3: Parametric Structural Canopy Documentation

## Table of Contents

- [Pseudo-Code](#pseudo-code)
- [Technical Explanation](#technical-explanation)
- [Design Variations](#design-variations)
- [Challenges and Solutions](#challenges-and-solutions)
- [References](#references)

---

## Pseudo-Code

### Pseudo-code: Canopy Structure Generation

1. **Main Function: Generating the Canopy**
   
   - **Inputs**:
     - `base_surface`: The initial surface for the canopy (Rhino.Geometry.Mesh).
     - `depth_map_control`: Control parameter for depth variation (e.g., from a slider).
     - `recursion_params`: Parameters for recursive supports, such as `depth`, `angle`, `length_multiplier`, etc.
     - `tessellation_strategy`: Strategy for surface tessellation (e.g., X, Y, diagonal lines).
     - `extrema_count`: The number of extrema points to generate supports from (based on a slider).

   - **Process**:
     1. **Generate Depth Map**:
        - Modify the `base_surface` by applying depth variations.
        - Use a control function to adjust surface heights based on `depth_map_control`.
     
     2. **Find Extremum Points**:
        - Calculate all extrema (global and local minima and maxima) on the modified surface.
        - Use the `find_all_extrema_points` function to identify points where supports will be generated.

     3. **Generate Recursive Supports**:
        - Use the extrema points to define where the supports should be placed.
        - Apply recursion to generate branching structures at the selected extrema points.
        - Parameters like `depth`, `branches`, `angle`, and `length_multiplier` control the support shape.

     4. **Adjust Surface Height**:
        - After generating the recursive supports, move the deformed surface to fit the support heights.
        - Use Grasshopper components to adjust the mesh height to ensure it aligns with the support structure.

     5. **Tessellate the Surface**:
        - Apply tessellation to the modified surface using a defined strategy (e.g., grid, diagonal, etc.).
        - Ensure the tessellation follows the surface shape and conforms to the support locations.

     6. **Apply Thickness to Supports and Tessellation**:
        - Pipe the generated curves (from tessellation and supports) to give them a defined thickness.
        - Use Grasshopper components to apply thickness to the curves and create a final canopy structure.

   - **Outputs**:
     - `canopy_mesh`: The final tessellated and thickened canopy mesh.
     - `supports`: The generated recursive support structures, possibly with thickness applied.

2. **Functions**

   - **`generate_depth_map(base_surface, control_value)`**
     - *Purpose*: Deform the input surface to introduce depth variation.
     - *Implementation*:
       - Adjust control points or apply a mathematical function (like sine or noise) to create a surface deformation based on `control_value`.

   - **`find_all_extrema_points(mesh)`**
     - *Purpose*: Identify global and local extrema points on the mesh surface.
     - *Implementation*:
       - Loop through mesh vertices, compare their Z-coordinates, and determine minima and maxima points.
       - Store global and local extrema points for further use.

   - **`generate_recursive_supports(start_point, params, depth)`**
     - *Purpose*: Generate branching support structures using recursion.
     - *Implementation*:
       - For each start point, generate a branch using `draw_tree_branch`.
       - Recursively call the function with reduced branch length and modified angles until the `depth` reaches zero.
       - Control the angle and number of branches at each recursion step to create a branching pattern.

   - **`tessellate_surface(surface, strategy)`**
     - *Purpose*: Tessellate the surface based on the chosen tessellation strategy.
     - *Implementation*:
       - Divide the surface into panels using the selected tessellation algorithm (e.g., X and Y lines, diagonal lines).
       - Apply non-uniform tessellation to ensure smooth transitions and fit with the support points.

   - **`Mesh Pipe)`**
     - *Purpose*: Apply a pipe to the tessellated and support curves to give them a defined thickness.
     - *Implementation*:
       - Use Grasshopper components to pipe the generated curves and create a solid structure.

---

## Technical Explanation

- **Depth Map Generation**
  - Explain how you manipulated the surface geometry.
      The input surface is first validated to ensure it is planar. It is then divided into a grid of points based on its domain and the specified number of divisions. These grid points act as control points for the surface deformation. Each grid point is displaced in the Z direction based on its proximity to attractor points. Attractors influence nearby points, creating localized bulges or depressions. After deformation, the modified grid points are used to construct a mesh. The vertices of the mesh are defined by the displaced points, and quadrilateral faces are added to connect adjacent points, forming a continuous surface.

  - Discuss the mathematical functions used (e.g., sine, cosine).
      Attractor Points: Attractor points serve as sources of deformation. The influence of an attractor on a grid point is inversely proportional to their distance, calculated using: 
      weight = 1 / (distance + ϵ)
      Here, 𝜖 is a small constant to prevent division by zero. This ensures that points closer to the attractor experience stronger deformation.

      Z-Direction Displacement: The vertical movement of each grid point is computed as: 
      movement = z_diff * weight * strength
      where z_diff is the vertical distance between the attractor and the grid point. The displacement is scaled by a strength parameter to control the intensity of deformation.

      Normalization: The total influence on each point is normalized by summing the weights of all attractors. This prevents over-amplification of deformation and ensures smooth transitions between affected and unaffected regions.

      Overshooting Prevention: To maintain natural deformation, the displacement of grid points is limited to avoid overshooting the attractor. Grid points move only toward or away from attractors without surpassing them.

  - Describe how control parameters affect the depth variations.
      Strength: The strength parameter directly controls the intensity of deformation. Higher values result in more pronounced bulges or depressions around the attractors, while lower values create subtler effects.

      Divisions: This parameter determines the resolution of the grid. A higher number of divisions produces a finer mesh with greater detail, capturing subtle variations. Conversely, fewer divisions result in a coarser mesh with less detail.

      Attractor Points: The location, number, and distribution of attractor points define the regions of deformation. Multiple attractors can create overlapping or distinct areas of influence, generating complex patterns.

      Distance Weighting: The use of inverse-distance weighting ensures that points farther from an attractor experience less deformation. This creates smooth, natural transitions across the surface, avoiding abrupt changes in geometry.

- **Surface Tessellation**
  - Describe the tessellation strategies implemented.
      The code employs horizontal, vertical, and diagonal tessellation lines projected onto a mesh using rg.Curve.ProjectToMesh. Horizontal and vertical lines are modulated by sine waves for non-uniform spacing, while diagonals span corner-to-corner, adding complexity.

  - Explain how tessellation contributes to the canopy design.
      Tessellation adapts to the mesh’s organic shape, ensuring alignment with its surface. Sine-modulated lines mimic natural rhythms, adding visual interest. Diagonal elements enhance the dynamic appearance and may provide structural reinforcement.

  - Discuss any algorithms or techniques used for non-uniform tessellation.
      Tessellation adapts to the mesh’s organic shape, ensuring alignment with its surface. Sine-modulated lines mimic natural rhythms, adding visual interest. Diagonal elements enhance the dynamic appearance and may provide structural reinforcement.


- **Recursive Supports Generation**
  - Explain how recursion was used to create complex support structures.
      The code uses recursion to generate tree-like branching structures. At each recursive step, a branch is created starting from a given point, extending in 3D space based on specified angles and lengths. Each branch splits into multiple smaller branches, creating a hierarchical pattern. The recursion stops when the depth reaches zero, representing the base case.

  - Discuss the parameters that control the recursion (e.g., depth, angle).
      Depth: Determines the number of recursive iterations, directly controlling the overall complexity and density of the structure.

      Angle (XY and Z): Controls the spatial orientation of branches. The angle_xy defines the spread in the XY plane, while angle_z adjusts the tilt relative to the Z-axis.

      Length Multiplier: Reduces the branch length with each recursive step, mimicking natural tapering seen in tree growth.

      Branches: Sets the number of branches at each node, affecting the density of the structure.

      Randomness: Optionally adds variation to branching angles, introducing organic irregularity.

  - Describe how branching patterns were achieved.
      Branching patterns are formed through iterative subdivision of branches. By default, branches are spaced evenly in the XY plane, creating symmetrical structures. The inclusion of a random offset adds natural variation, enhancing the organic appearance. The combination of controlled parameters, such as depth and length reduction, creates a visually coherent yet intricate network of supports.

---

## Design Variations

### Base Surface Variations

1. **Variation 1**

   ![Base Surface 1](images/Base_Surface_1.jpg)
   ![Depth map 1](images/Depth_Map_1.jpg)
   ![Canopy 1](images/Final_Structure_1.jpg)

   - **Parameters**:
     - Points in rhino
     - `Strength`: [1.0]

2. **Variation 2**

   ![Base Surface 2](images/Base_Surface_2.jpg)
   ![Depth map 2](images/Depth_Map_2.jpg)
   ![Canopy 2](images/Final_Structure_2.jpg)

   - **Parameters**:
     - Points in rhino
     - `Strength`: [2.0]

3. **Variation 3**

   ![Base Surface 3](images/Base_Surface_3.jpg)
   ![Depth map 3](images/Depth_Map_3.jpg)
   ![Canopy 3](images/Final_Structure_3.jpg)

   - **Parameters**:
     - Points in rhino
     - `Strength`: [1.5]

### Tessellation Variations

1. **Variation 1**

   ![Tessellation 1](images/Tessellation_Curves_1.jpg)

   - **Parameters**:
     - `Resulution`: [44]
     - `Frequency`: [50]
     - `Amplitude`: [20]

2. **Variation 2**

   ![Tessellation 2](images/Tessellation_Curves_2.jpg)

   - **Parameters**:
     - `Resulution`: [60]
     - `Frequency`: [42]
     - `Amplitude`: [40]

3. **Variation 3**

   ![Tessellation 3](images/Tessellation_Curves_3.jpg)

   - **Parameters**:
     - `Resulution`: [32]
     - `Frequency`: [43]
     - `Amplitude`: [4]

### Recursive Supports Variations

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

- **Challenge 1**: Having a vision or inspiration, and not knowing how to make it.
  - **Solution**: I made something else.

- **Challenge 2**: Not knowing how to debug and fix the errors in my code.
  - **Solution**: I got ChatGPT to explain it to me and sometimes help me fix the errors.

- **Challenge 3**: Not being able to make a non-planar voronoi.
  - **Solution**: I decided to not make a voronoi.

---

## References

- Random
- NumPy
- Rhino.Python Guides
- RhinoScriptSyntax Documentation
- ChatGPT

---