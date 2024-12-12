# Introduction
## Purpose

The project provides a modular implementation for handling, analyzing, scaling, and visualizing human poses detected using OpenPose. The framework supports both data manipulation and visualization, enabling users to scale poses based on demographic attributes (age and gender), infer attributes like posture, and render poses as images. It aims to serve applications in motion analysis, character design, and pose normalization across various domains.
Main Functionality

- Pose Representation: Encodes individual poses, including body, face, hands, and feet keypoints, with mechanisms to convert to/from OpenPose-compatible JSON.
- Attribute Estimation: Offers heuristics to estimate age, gender, posture, and height based on pose keypoints and proportions.
-  Scaling and Transformation: Provides tools to scale poses dynamically, considering differences in age, gender, and height, while maintaining realistic proportions.
-  Visualization: Renders poses on a canvas, with support for body graphs and color-coded anatomical regions.
-  Data Integration: Handles multiple poses within a scene, supporting file operations (load, save, and merge) and comprehensive visualization of entire canvases.

## Key Insights: WHO Data and Heuristics
### WHO Data Integration

The framework incorporates age and gender-specific height data derived from World Health Organization (WHO) guidelines to ensure realistic scaling. Key insights include:

- Smoothed Height Progression: Height data is smoothed across age groups to provide reliable estimates for proportions during scaling.
- Adaptability: The framework clamps age values outside the supported range to the nearest boundary, ensuring robustness for atypical inputs.
- Reference Proportions: Age-specific proportions (e.g., head-to-torso ratios) align with height data to enhance accuracy in scaling operations.

### Heuristics for Estimation

The project employs heuristics to infer attributes like posture, age, and gender, balancing simplicity and effectiveness:

- Posture Detection: A multi-step heuristic examines spatial relationships between keypoints (e.g., ankle position for standing, hip-to-knee alignment for sitting) to deduce posture. Missing keypoints are handled gracefully, with fallback assumptions (e.g., vertical alignment implies standing).
- Age and Gender: Ratios of limb lengths and torso dimensions guide the estimation of demographic attributes. For example, longer leg-to-torso ratios indicate male adults, while higher head-to-body ratios suggest younger children.
- Real-World Context: The heuristics aim to approximate real-world observations, using empirical knowledge of human anatomy and movement.

### Strengths of the Approach

- Data-Driven: WHO data grounds the scaling and height estimation in real-world statistics, enhancing realism and applicability.
- Flexibility: The heuristic-driven approach accommodates incomplete or ambiguous input data, making it robust for diverse scenarios.
- Modularity: Decoupled modules and functions ensure maintainability, extendability, and usability in various contexts.

# Example usage
Here's an example usage demonstrating how to load OpenPose data, scale the poses by a specified age and gender, and save the updated OpenPose data back to a file:

```python
from OpenPose import OpenPose
from anchor_point import dict_to_keypoints_array, choose_main_support_with_gravity
from scaling import get_scaling_factors
import logging

# Configure the logging level and format
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to see all debug messages
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Example usage
def main():
    # File paths
    input_file = "Female_10yo_standing_00001.json"
    output_file = "Female_10yo_standing_00001_f20.json"
    output_image = "Female_10yo_standing_00001_f20.png"

    # Parameters for scaling
    target_age = 20
    target_gender = "female"

    # Step 1: Load OpenPose data from a JSON file
    openpose_data = OpenPose.load(input_file)
    openpose_data.save_as_image("input.png")

    print(openpose_data.people[0].face)
    print(openpose_data.people[0].guess_age())
    
    print(get_scaling_factors(target_age,target_gender))

    anchor = choose_main_support_with_gravity( dict_to_keypoints_array(openpose_data.people[0].body) )
    print(f"anchor: {anchor}")

    openpose_data.people[0].input_age = 10
    openpose_data.people[0].input_gender = "female"

    # Step 2: Scale all poses in the OpenPose data
    for index, pose in enumerate(openpose_data.people):
        print(f"Scaling pose {index} to target age {target_age} and gender {target_gender}.")
        openpose_data.scale_pose(index, target_gender=target_gender, target_age=target_age)

    
    print(openpose_data.people[0].face)

    # Step 3: Save the scaled OpenPose data back to a JSON file
    openpose_data.save(output_file)
    openpose_data.save_as_image(output_image)
    
if __name__ == "__main__":
    main()
```

Explanation:
1. Loading Data:
The OpenPose.load() method reads the OpenPose-compatible JSON data and constructs an OpenPose object with multiple Pose instances.
2. Scaling Poses:
The scale_pose() method is called for each pose in openpose_data.people. It uses the target age and gender to adjust the pose proportions and dimensions dynamically.
3. Saving Data:
The OpenPose.save() method writes the updated poses into a JSON file in OpenPose's original format.


