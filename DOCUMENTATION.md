# Assignment 3: Parametric Structural Canopy Documentation

## Table of Contents

- [Pseudo-Code](#pseudo-code)
- [Technical Explanation](#technical-explanation)
- [Design Variations](#design-variations)
- [Challenges and Solutions](#challenges-and-solutions)
- [References](#references)

---

## Pseudo-Code

*(Provide detailed pseudo-code explaining the logic of your program. Outline your functions for depth map generation, recursive geometry, and tessellation, and how they contribute to the final structural canopy.)*

### Example Structure:

1. **Main Function: Generating the Canopy**

   - **Inputs**:
     - `base_surface`: The initial surface for the canopy.
     - `depth_map_control`: Control parameter for depth variation.
     - `recursion_params`: Parameters for recursive supports.
     - `tessellation_strategy`: Strategy for surface tessellation.
     - `support_points`: Points where supports will be generated.

   - **Process**:
     - **Generate Depth Map**:
       - Modify `base_surface` using a control function.
     - **Tessellate Surface**:
       - Divide the modified surface into panels.
     - **Generate Vertical Supports**:
       - Create supports using recursive geometry.

   - **Outputs**:
     - `canopy_mesh`: The tessellated canopy shell.
     - `supports`: The vertical support structures.

2. **Functions**

   - **`generate_depth_map(surface, control_value)`**
     - *Purpose*: Modify the input surface to create depth variations.
     - *Implementation Details*:
       - Use mathematical functions to adjust control points.
       - Explore different methods for depth manipulation.

   - **`tessellate_surface(surface, strategy)`**
     - *Purpose*: Tessellate the surface based on the chosen strategy.
     - *Implementation Details*:
       - Implement grid-based, triangular, Voronoi, or other tessellation algorithms.
       - Ensure non-uniformity in the tessellation pattern.

   - **`generate_recursive_supports(start_point, params, depth)`**
     - *Purpose*: Generate branching structures for supports.
     - *Implementation Details*:
       - Use recursion to create complex geometries.
       - Control recursion with parameters like `max_depth` and `angle`.

---

## Technical Explanation

*(Provide a concise explanation of your code, focusing on how you implemented depth map manipulation, recursive geometry generation, and surface tessellation in Grasshopper Python. Discuss how your approach generates the final structural canopy and the mathematical principles involved.)*

### Topics to Cover:

- **Depth Map Generation**
  - Explain how you manipulated the surface geometry.
  - Discuss the mathematical functions used (e.g., sine, cosine).
  - Describe how control parameters affect the depth variations.

- **Surface Tessellation**
  - Describe the tessellation strategies implemented.
  - Explain how tessellation contributes to the canopy design.
  - Discuss any algorithms or techniques used for non-uniform tessellation.

- **Recursive Supports Generation**
  - Explain how recursion was used to create complex support structures.
  - Discuss the parameters that control the recursion (e.g., depth, angle).
  - Describe how branching patterns were achieved.

- **Combining Geometries**
  - Explain the methods used to integrate the shell and supports.
  - Discuss any challenges in merging different geometries.

---

## Design Variations

*(Include images and descriptions of your generated design variations. For each category, provide at least three variations and discuss the differences and design decisions.)*

### Base Surface Shape Variations

1. **Variation 1: [Name/Description]**

   ![Canopy Variation 1](images/canopy.jpg)

   - **Parameters**:
     - `control_value`: [Value]
     - Other relevant parameters.

2. **Variation 2: [Name/Description]**

   ![Canopy Variation 2](images/canopy.jpg)

   - **Parameters**:
     - `control_value`: [Value]
     - Other relevant parameters.

3. **Variation 3: [Name/Description]**

   ![Canopy Variation 3](images/canopy.jpg)

   - **Parameters**:
     - `control_value`: [Value]
     - Other relevant parameters.

*(Repeat for Surface Tessellation Pattern and Vertical Supports.)*

---

## Challenges and Solutions

*(Discuss any challenges you faced during the assignment and how you overcame them.)*

### Examples:

- **Challenge 1**: Adapting scripts to Grasshopper.
  - **Solution**: Describe how you addressed this challenge, such as learning the Rhino.Geometry module or adjusting data types.

- **Challenge 2**: Managing data structures.
  - **Solution**: Explain the strategies you used to handle lists and trees in Grasshopper.

- **Challenge 3**: Performance optimization.
  - **Solution**: Discuss how you optimized your code to run efficiently.

---

## References

*(List any resources you used or found helpful during the assignment.)*

- **Python for CAD Applications**:
  - Rhino.Python Guides
  - RhinoScriptSyntax Documentation

- **Grasshopper and GhPython**:
  - Grasshopper Primer
  - GhPython Tutorials

- **Mathematical Functions and Recursion**:
  - Python Math Module
  - Recursion in Python Tutorials

- **Surface Tessellation Techniques**:
  - Voronoi Diagrams
  - Delaunay Triangulation


Inspiration:
- https://en.idei.club/35099-voronoi-generation.html
- https://parametrichouse.com/voronoi-architecture/
- https://link.springer.com/article/10.1007/s00004-018-0383-y

References:
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html
- Random
- NumPy
- Rhino.Python Guides
- RhinoScriptSyntax Documentation
- ChatGPT

---

*(Feel free to expand upon these sections to fully capture your work and learning process.)*
