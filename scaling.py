from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import logging

def get_height_by_age_gender(age, gender):
    """
    Estimates the height (in cm) based on age and gender using smoothed values.

    Parameters:
        age (int): Age of the person.
        gender (str): Gender of the person ("male" or "female").

    Returns:
        float: Estimated height in cm.
    """
    # WHO-based average heights for different ages
    height_data = {
        "male": {
            1: 75.0, 2: 87.0, 3: 96.0, 4: 102.0, 5: 108.0, 6: 115.0,
            7: 120.0, 8: 125.0, 9: 130.0, 10: 137.0, 11: 143.0, 12: 149.0,
            13: 156.0, 14: 163.0, 15: 169.0, 16: 173.0, 17: 175.0,
            18: 176.0, 19: 176.0, 20: 176.0,  # Adult height
        },
        "female": {
            1: 74.0, 2: 85.0, 3: 95.0, 4: 100.0, 5: 106.0, 6: 113.0,
            7: 118.0, 8: 123.0, 9: 129.0, 10: 135.0, 11: 141.0, 12: 148.0,
            13: 155.0, 14: 160.0, 15: 163.0, 16: 164.0, 17: 164.0,
            18: 165.0, 19: 165.0, 20: 165.0,  # Adult height
        },
    }

    # Ensure the age is within bounds
    age_data = height_data.get(gender, height_data["female"])
    
    # Adult fallback
    if age >= 20:
        return age_data[20]  # Return the adult height

    if age in age_data:
        return age_data[age]

    # Clamp to min and max ages
    min_age, max_age = min(age_data.keys()), max(age_data.keys())
    if age < min_age:
        return age_data[min_age]
    elif age > max_age:
        return age_data[max_age]

    # Shouldn't happen due to exhaustive age data
    raise ValueError("Unexpected age value not covered in height data.")

def get_edge_factor(start: str, end: str, scaling_factors: Dict[str, float]) -> float:
    """
    Get the scaling factor for a given connection between two body points.

    Parameters:
        start (str): The starting keypoint (e.g., "Neck").
        end (str): The ending keypoint (e.g., "Nose").
        scaling_factors (Dict[str, float]): Precomputed scaling factors for the target age and gender.

    Returns:
        float: The scaling factor for the connection.
    """
    # Define a connection-to-ratio mapping
    connection_map = {
        # Head and torso
        ("Neck", "Nose"): scaling_factors["head_ratio"],
        ("Neck", "RShoulder"): scaling_factors["torso_ratio"],
        ("Neck", "LShoulder"): scaling_factors["torso_ratio"],
        ("Neck", "RHip"): scaling_factors["torso_ratio"],
        ("Neck", "LHip"): scaling_factors["torso_ratio"],
        
        # Arms
        ("RShoulder", "RElbow"): scaling_factors["arm_ratio"],
        ("RElbow", "RWrist"): scaling_factors["arm_ratio"],
        ("LShoulder", "LElbow"): scaling_factors["arm_ratio"],
        ("LElbow", "LWrist"): scaling_factors["arm_ratio"],

        # Legs
        ("RHip", "RKnee"): scaling_factors["leg_ratio"],
        ("RKnee", "RAnkle"): scaling_factors["leg_ratio"],
        ("LHip", "LKnee"): scaling_factors["leg_ratio"],
        ("LKnee", "LAnkle"): scaling_factors["leg_ratio"],

        # Face
        ("Nose", "REye"): scaling_factors["head_ratio"],
        ("Nose", "LEye"): scaling_factors["head_ratio"],
        ("REye", "REar"): scaling_factors["head_ratio"],
        ("LEye", "LEar"): scaling_factors["head_ratio"],
    }

    # Ensure bidirectional lookup
    if (start, end) in connection_map:
        return connection_map[(start, end)]
    if (end, start) in connection_map:
        return connection_map[(end, start)]

    # Default to head ratio for unexpected connections
    return scaling_factors["head_ratio"]

    
def get_scaling_factors(age: int, gender: str = "female") -> Dict[str, float]:
    """
    Returns scaling factors for body and facial proportions based on age and gender.

    Parameters:
        age (int): The target age for scaling.
        gender (str): The target gender for scaling ("male" or "female").

    Returns:
        Dict[str, float]: A dictionary of scaling factors for various body regions.
    """
    if gender not in ["male", "female"]:
        raise ValueError("`gender` must be either 'male' or 'female'.")
    if not (0 <= age <= 120):
        raise ValueError("`age` must be between 0 and 120.")

    # Base adult proportions for reference
    scaling_factors = {
        "head_ratio": 0.15, "torso_ratio": 0.36, "arm_ratio": 0.20, "leg_ratio": 0.30,
        "hand_ratio": 1.0, "foot_ratio": 1.0, "eye_factor": 1.0, "mouth_factor": 1.0,
        "jaw_factor": 1.0, "nose_factor": 1.0, "face_contour_factor": 1.0,
    }

    # Define age ranges for adjustments
    age_ranges = [
        (0, 5, {
            "head_ratio": 0.25, "torso_ratio": 0.30, "arm_ratio": 0.15, "leg_ratio": 0.30,
            "hand_ratio": 0.8, "foot_ratio": 0.8, "eye_factor": 1.5, "mouth_factor": 1.2,
            "jaw_factor": 1.3, "nose_factor": 0.8, "face_contour_factor": 1.4,
        }),
        (6, 7, {
            "head_ratio": 0.23, "torso_ratio": 0.32, "arm_ratio": 0.17, "leg_ratio": 0.29,
            "hand_ratio": 0.85, "foot_ratio": 0.85, "eye_factor": 1.4, "mouth_factor": 1.1,
            "jaw_factor": 1.2, "nose_factor": 0.85, "face_contour_factor": 1.3,
        }),
        (8, 10, {
            "head_ratio": 0.21, "torso_ratio": 0.34, "arm_ratio": 0.18, "leg_ratio": 0.28,
            "hand_ratio": 0.9, "foot_ratio": 0.9, "eye_factor": 1.3, "mouth_factor": 1.1,
            "jaw_factor": 1.15, "nose_factor": 0.9, "face_contour_factor": 1.2,
        }),
        (11, 13, {
            "head_ratio": 0.19, "torso_ratio": 0.35, "arm_ratio": 0.19, "leg_ratio": 0.27,
            "hand_ratio": 1.0, "foot_ratio": 1.0, "eye_factor": 1.2, "mouth_factor": 1.1,
            "jaw_factor": 1.05, "nose_factor": 1.0, "face_contour_factor": 1.1,
        }),
        (14, 16, {
            "head_ratio": 0.17, "torso_ratio": 0.36, "arm_ratio": 0.19, "leg_ratio": 0.28,
            "hand_ratio": 1.05, "foot_ratio": 1.05, "eye_factor": 1.1, "mouth_factor": 1.1,
            "jaw_factor": 1.0, "nose_factor": 1.0, "face_contour_factor": 1.05,
        }),
        (17, 19, {
            "head_ratio": 0.17, "torso_ratio": 0.36, "arm_ratio": 0.20, "leg_ratio": 0.29,
            "hand_ratio": 1.1, "foot_ratio": 1.1, "eye_factor": 1.0, "mouth_factor": 1.0,
            "jaw_factor": 1.0, "nose_factor": 1.0, "face_contour_factor": 1.05,
        }),
    ]

    # Apply adjustments based on age
    for min_age, max_age, adjustments in age_ranges:
        if min_age <= age <= max_age:
            scaling_factors.update(adjustments)
            break

    # Apply gender-based adjustments
    if gender == "female":
        scaling_factors["jaw_factor"] *= 0.95  # Softer jawline
        scaling_factors["mouth_factor"] *= 1.1  # Larger lips
        scaling_factors["face_contour_factor"] *= 1.05  # Rounder face contour

    return scaling_factors


def scale_face(
    face_points: List[Optional[Tuple[float, float]]],
    scaling_factors: dict,
    height_ratio: float,
    scaled_keypoints: Dict[str, Tuple[float, float]],
    original_keypoints: Dict[str, Tuple[float, float]],
) -> List[Optional[Tuple[float, float]]]:
    """
    Scales and aligns facial keypoints based on scaled and original body keypoints.

    Parameters:
        face_points (List[Optional[Tuple[float, float]]]): List of original facial keypoints.
        scaling_factors (dict): Scaling factors for different facial regions.
        height_ratio (float): Ratio of target height to input height.
        scaled_keypoints (Dict[str, Tuple[float, float]]): Dictionary of scaled body keypoints.
        original_keypoints (Dict[str, Tuple[float, float]]): Dictionary of original body keypoints.

    Returns:
        List[Optional[Tuple[float, float]]]: Scaled and aligned facial keypoints.
    """

    if not face_points or all(point is None for point in face_points):
        logging.warning("No face points to scale.")
        return face_points  # No scaling if no valid points

    def calculate_mouth_center(face_points, indices=range(48, 68)):
        """
        Calculates the center of the mouth as the mean position of valid points in the specified range.

        Parameters:
            face_points (List[Optional[Tuple[float, float]]]): List of facial keypoints.
            indices (range): Range of indices representing the mouth region.

        Returns:
            Optional[Tuple[float, float]]: Calculated center of the mouth, or None if no valid points.
        """
        valid_points = [face_points[i] for i in indices if face_points[i] is not None]
        if not valid_points:
            return None
        cx = sum(p[0] for p in valid_points) / len(valid_points)
        cy = sum(p[1] for p in valid_points) / len(valid_points)
        return (cx, cy)

    mouth_center = calculate_mouth_center(face_points)
    if mouth_center:
        scaled_mouth_center = (
            scaled_keypoints["Nose"][0] + (mouth_center[0] - original_keypoints["Nose"][0]) * height_ratio,
            scaled_keypoints["Nose"][1] + (mouth_center[1] - original_keypoints["Nose"][1]) * height_ratio,
        )
    else:
        logging.warning("Mouth center could not be calculated; skipping mouth scaling.")
        scaled_mouth_center = None

    # Define facial regions based on COCO format
    regions = {
        # Face contour (0-16 inclusive)
        "face_contour": ([0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16], "Nose", "face_contour_factor"),
        # Jaw (6-10 inclusive)
        "jaw": (range(6, 11), "Nose", "jaw_factor"),
        # Right eyebrow (17-21 inclusive)
        "right_eyebrow": (range(17, 22), "REye", "eye_factor"),
        # Left eyebrow (22-26 inclusive)
        "left_eyebrow": (range(22, 27), "LEye", "eye_factor"),
        # Nose (27-35 inclusive)
        "nose": (range(27, 36), "Nose", "nose_factor"),
        # Right eye (36-41 inclusive)
        "right_eye": (range(36, 42), "REye", "eye_factor"),
        # Left eye (42-47 inclusive)
        "left_eye": (range(42, 48), "LEye", "eye_factor"),
        # Mouth (48-70 inclusive)
        "mouth": (range(48, 71), scaled_mouth_center, "mouth_factor"),
    }


    def scale_region(indices: range, base_keypoint: Union[str, Tuple[float, float]], factor_key: str):
        """
        Scale a region of facial points around a base position.

        Parameters:
            indices (range): Indices of points in the region.
            base_keypoint (Union[str, Tuple[float, float]]): Keypoint in `scaled_keypoints` 
                                                            or a calculated tuple used as the alignment base.
            factor_key (str): Key to fetch the scaling factor for this region.
        """
        if isinstance(base_keypoint, str):
            scaled_base = scaled_keypoints.get(base_keypoint)
            original_base = original_keypoints.get(base_keypoint)
        else:
            scaled_base = base_keypoint
            original_base = mouth_center  # Use the calculated mouth center for mouth region

        if not scaled_base or not original_base:
            logging.warning(f"Base keypoint {base_keypoint} missing for scaling {factor_key}.")
            return

        sx, sy = scaled_base
        ox, oy = original_base
        scaling_factor = scaling_factors.get(factor_key, 1.0)

        for i in indices:
            if i < len(face_points) and face_points[i] is not None:
                x, y = face_points[i]
                dx, dy = x - ox, y - oy
                face_points[i] = (
                    sx + dx * scaling_factor * height_ratio,
                    sy + dy * scaling_factor * height_ratio,
                )
                logging.debug(
                    f"Scaled point {i} in region '{factor_key}' using base {base_keypoint}: "
                    f"original_base=({ox}, {oy}), scaled_base=({sx}, {sy}), "
                    f"original=({x}, {y}), scaled=({face_points[i][0]}, {face_points[i][1]})"
                )

    # Apply scaling to all defined regions
    for region_name, (indices, base_keypoint, factor_key) in regions.items():
        logging.info(f"Scaling region '{region_name}' with base '{base_keypoint}' and factor '{factor_key}'.")
        scale_region(indices, base_keypoint, factor_key)

    # Convert to tuples of float for consistency
    face_points = [
        (float(point[0]), float(point[1])) if point is not None else None for point in face_points
    ]

    return face_points

# Define scaling and alignment function for hands and feet
def scale_and_align_points(
    points: List[Optional[Tuple[float, float]]],
    scaling_factor: float,
    scaled_base: Tuple[float, float],
    original_base: Tuple[float, float],
) -> List[Optional[Tuple[float, float]]]:
    """
    Scales and aligns a set of points relative to the original and scaled base points.

    Parameters:
        points (List[Optional[Tuple[float, float]]]): List of points to scale and align.
        scaling_factor (float): Scaling factor for the region.
        scaled_base (Tuple[float, float]): Scaled position of the base keypoint.
        original_base (Tuple[float, float]): Original position of the base keypoint.

    Returns:
        List[Optional[Tuple[float, float]]]: Scaled and aligned points.
    """
    if not points or not scaled_base or not original_base:
        logging.warning("Skipping scaling: invalid base keypoint or empty points.")
        return points

    scaled_points = []
    for point in points:
        if point is not None:
            dx, dy = point[0] - original_base[0], point[1] - original_base[1]
            scaled_points.append((
                scaled_base[0] + dx * scaling_factor,
                scaled_base[1] + dy * scaling_factor
            ))
        else:
            scaled_points.append(None)
    return scaled_points
