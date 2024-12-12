from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np
import logging

from anchor_point import choose_main_support_with_gravity, dict_to_keypoints_array
from scaling import *

connections = {
    "Neck": ["Nose", "RShoulder", "LShoulder", "RHip", "LHip"],
    "RShoulder": ["RElbow", "Neck"],
    "RElbow": ["RWrist", "RShoulder"],
    "RWrist": ["RElbow"],
    "LShoulder": ["LElbow", "Neck"],
    "LElbow": ["LWrist", "LShoulder"],
    "LWrist": ["LElbow"],
    "RHip": ["RKnee", "Neck"],
    "RKnee": ["RAnkle", "RHip"],
    "RAnkle": ["RKnee"],
    "LHip": ["LKnee", "Neck"],
    "LKnee": ["LAnkle", "LHip"],
    "LAnkle": ["LKnee"],
    "Nose": ["Neck", "REye", "LEye"],
    "REye": ["Nose", "REar"],
    "LEye": ["Nose", "LEar"],
    "REar": ["REye"],
    "LEar": ["LEye"]
}

@dataclass
class Pose:
    """
    Represents the data of a single entry in the "people" key of an OpenPose JSON.
    """
    body: Dict[str, Tuple[float, float]] = field(default_factory=dict)
    face: List[Optional[Tuple[float, float]]] = field(default_factory=list)
    right_hand: List[Optional[Tuple[float, float]]] = field(default_factory=list)
    left_hand: List[Optional[Tuple[float, float]]] = field(default_factory=list)
    right_foot: List[Optional[Tuple[float, float]]] = field(default_factory=list)
    left_foot: List[Optional[Tuple[float, float]]] = field(default_factory=list)
    canvas_width: int = None
    canvas_height: int = None
    input_gender: Optional[str] = None
    input_age: Optional[int] = None

    def to_json(self) -> Dict:
        """Converts the Pose object to OpenPose-compatible JSON."""
        def points_to_flat(points: List[Optional[Tuple[float, float]]]) -> List[float]:
            return [
                coord for point in points for coord in (point + (1.0,) if point else (0.0, 0.0, 0.0))
            ]

        return {
            "pose_keypoints_2d": [
                coord
                for key in self.body.keys() if self.body[key] is not None
                for coord in (self.body[key] + (1.0,))
            ],
            "face_keypoints_2d": points_to_flat(self.face),
            "hand_right_keypoints_2d": points_to_flat(self.right_hand),
            "hand_left_keypoints_2d": points_to_flat(self.left_hand),
            "foot_right_keypoints_2d": points_to_flat(self.right_foot),
            "foot_left_keypoints_2d": points_to_flat(self.left_foot)
        }

    @classmethod
    def from_json(cls, data: Dict, canvas_width, canvas_height) -> "Pose":
        """Creates a Pose object from OpenPose-compatible JSON."""
        if not isinstance(data, dict) or "pose_keypoints_2d" not in data:
            raise ValueError("Invalid OpenPose JSON structure.")

        def flat_to_points(flat_list: List[float], points_per_part: int) -> List[Optional[Tuple[float, float]]]:
            return [
                (flat_list[i], flat_list[i + 1]) if flat_list[i + 2] > 0.0 else None
                for i in range(0, len(flat_list), 3)
            ]

        return cls(
            body={
                key: (data["pose_keypoints_2d"][i * 3], data["pose_keypoints_2d"][i * 3 + 1])
                for i, key in enumerate([
                    "Nose", "Neck", "RShoulder", "RElbow", "RWrist",
                    "LShoulder", "LElbow", "LWrist", "RHip", "RKnee",
                    "RAnkle", "LHip", "LKnee", "LAnkle", "REye",
                    "LEye", "REar", "LEar"
                ])
                if data["pose_keypoints_2d"][i * 3 + 2] > 0.0
            },
            face=flat_to_points(data.get("face_keypoints_2d", []), 70),
            right_hand=flat_to_points(data.get("hand_right_keypoints_2d", []), 21),
            left_hand=flat_to_points(data.get("hand_left_keypoints_2d", []), 21),
            right_foot=flat_to_points(data.get("foot_right_keypoints_2d", []), 21),
            left_foot=flat_to_points(data.get("foot_left_keypoints_2d", []), 21),
            canvas_width=canvas_width,
            canvas_height=canvas_height
        )

    def guess_gender(self) -> Optional[str]:
        """
        Guesses the gender based on limb proportions.
        If input_gender is already set, return it.

        Returns:
            Optional[str]: Guessed or set gender ("male" or "female").
        """
        if self.input_gender:
            return self.input_gender

        def calculate_distance(p1, p2):
            """Helper function to calculate the Euclidean distance between two points."""
            return np.hypot(p2[0] - p1[0], p2[1] - p1[1])

        body = self.body

        if all(k in body for k in ["Neck", "RHip", "RKnee", "RAnkle"]):
            torso_length = calculate_distance(body["Neck"], body["RHip"])
            leg_length = calculate_distance(body["RHip"], body["RKnee"]) + \
                        calculate_distance(body["RKnee"], body["RAnkle"])
        else:
            return None  # Insufficient data to estimate gender

        # Simple heuristic: males typically have longer legs relative to torso length
        if torso_length > 0:
            leg_to_torso_ratio = leg_length / torso_length
            return "male" if leg_to_torso_ratio > 1.5 else "female"
        return None

    def guess_age(self) -> Optional[int]:
        """
        Estimates the age of a person based on the torso-to-head ratio.

        Returns:
            Optional[int]: Estimated age in years or None if estimation is not possible.
        """
        def calculate_distance(p1, p2):
            """Helper function to calculate the Euclidean distance between two points."""
            return np.hypot(p2[0] - p1[0], p2[1] - p1[1])

        # Extract torso and head measurements
        body = self.body

        if "Neck" in body and "Nose" in body:
            head_length = calculate_distance(body["Neck"], body["Nose"])
        else:
            logging.warning("Head length cannot be measured; missing 'Neck' or 'Nose'.")
            return None

        if "Neck" in body and "RHip" in body and "LHip" in body:
            torso_length = calculate_distance(body["Neck"], body["RHip"]) / 2 + \
                        calculate_distance(body["Neck"], body["LHip"]) / 2
        else:
            logging.warning("Torso length cannot be measured; missing 'Neck' or 'Hips'.")
            return None

        # Calculate the torso-to-head ratio
        torso_to_head_ratio = torso_length / head_length

        # Reference gender for age scaling
        reference_gender = self.guess_gender() or "female"

        # Use get_scaling_factors to retrieve predefined ratios
        age_to_ratios = {}
        for age in range(0, 21):  # Predefined ages from 0 to 20
            scaling_factors = get_scaling_factors(age, reference_gender)
            age_to_ratios[age] = scaling_factors["torso_ratio"] / scaling_factors["head_ratio"]

        # Find the closest matching age
        best_match = None
        min_difference = float("inf")
        for age, ratio in age_to_ratios.items():
            difference = abs(torso_to_head_ratio - ratio)
            if difference < min_difference:
                min_difference = difference
                best_match = age

        logging.info(f"Estimated age: {best_match} (Torso-to-Head Ratio: {torso_to_head_ratio:.3f})")
        return best_match

    def estimate_height(self) -> Optional[float]:
        """
        Estimates the height of a person based on the estimated age and gender.

        Returns:
            Optional[float]: Estimated height in cm, or None if estimation fails.
        """
        # Step 1: Estimate age
        age = self.guess_age()
        if age is None:
            logging.warning("Age estimation failed.")
            return None

        # Step 2: Guess gender
        gender = self.guess_gender() or "female"  # Default to "female" if gender can't be guessed

        # Step 3: Use pre-defined height averages
        height = get_height_by_age_gender(age, gender)
        logging.info(f"Estimated height for age {age} and gender {gender}: {height} cm")
        return height


    def scale(self, target_gender: str, target_age: int) -> "Pose":
        input_age = self.input_age or self.guess_age()
        input_gender = self.input_gender or self.guess_gender()

        input_scaling_factors = get_scaling_factors(input_age, input_gender)
        target_scaling_factors = get_scaling_factors(target_age, target_gender)

        # uncomment for testing purposes: ignore age related proportion changes and only scale by height
        """
        target_scaling_factors = {
            "head_ratio": 0.15,
            "torso_ratio": 0.36,
            "arm_ratio": 0.20,
            "leg_ratio": 0.30,
            "hand_ratio": 1.0,
            "foot_ratio": 1.0,
            "eye_factor": 1.0,
            "mouth_factor": 1.0,
            "jaw_factor": 1.0,
            "nose_factor": 1.0,
            "face_contour_factor": 1.0,
        }
        """
        
        adjusted_scaling_factors = {
            key: target_scaling_factors[key] / input_scaling_factors[key]
            for key in input_scaling_factors.keys()
        }

        input_height = get_height_by_age_gender(input_age, input_gender)
        target_height = get_height_by_age_gender(target_age, target_gender)
        height_ratio = target_height / input_height if input_height > 0 else 1.0

        # Detect anchor point
        anchor = choose_main_support_with_gravity(dict_to_keypoints_array(self.body))

        # Flatten connections into a list of edges
        edges = [(start, end) for start, connections_list in connections.items() for end in connections_list]

        # Initialize scaled keypoints with the anchor point
        scaled_keypoints = {anchor: np.array(self.body[anchor])}
        visited = set([anchor])  # Track visited keypoints to prevent redundant calculations
        queue = [anchor]  # Initialize queue for BFS traversal

        # Process edges in a breadth-first manner
        while queue:
            current = queue.pop(0)  # Get the current keypoint
            for connection in connections.get(current, []):
                if connection not in visited and connection in self.body:
                    # Calculate the scaled position for the connection
                    start_pos = scaled_keypoints[current]
                    end_pos = np.array(self.body[connection])
                    vector = end_pos - np.array(self.body[current])
                    norm = np.linalg.norm(vector)

                    if norm > 1e-6:
                        direction = vector / norm
                        edge_factor = get_edge_factor(current, connection, adjusted_scaling_factors)
                        scaled_length = norm * edge_factor * height_ratio
                        scaled_vector = direction * scaled_length

                        # Store the scaled position
                        scaled_keypoints[connection] = tuple(float(coord) for coord in (start_pos + scaled_vector))
                        visited.add(connection)
                        queue.append(connection)

        new_face = scale_face(self.face, adjusted_scaling_factors, height_ratio, scaled_keypoints, self.body)

        # Scale and align left hand
        new_left_hand = scale_and_align_points(
            self.left_hand,
            adjusted_scaling_factors["hand_ratio"] * height_ratio,
            scaled_keypoints.get("LWrist"),
            self.body.get("LWrist"),
        )

        # Scale and align right hand
        new_right_hand = scale_and_align_points(
            self.right_hand,
            adjusted_scaling_factors["hand_ratio"] * height_ratio,
            scaled_keypoints.get("RWrist"),
            self.body.get("RWrist"),
        )

        # Scale and align left foot
        new_left_foot = scale_and_align_points(
            self.left_foot,
            adjusted_scaling_factors["foot_ratio"] * height_ratio,
            scaled_keypoints.get("LAnkle"),
            self.body.get("LAnkle"),
        )

        # Scale and align right foot
        new_right_foot = scale_and_align_points(
            self.right_foot,
            adjusted_scaling_factors["foot_ratio"] * height_ratio,
            scaled_keypoints.get("RAnkle"),
            self.body.get("RAnkle"),
        )

        # Crop to canvas
        def crop_point(point):
            return (
                max(0, min(self.canvas_width, point[0])),
                max(0, min(self.canvas_height, point[1]))
            )

        for key in scaled_keypoints:
            if scaled_keypoints[key] is not None:
                scaled_keypoints[key] = crop_point(scaled_keypoints[key])

        new_face = [crop_point(p) if p is not None else None for p in new_face]
        new_left_hand = [crop_point(p) if p is not None else None for p in new_left_hand]
        new_right_hand = [crop_point(p) if p is not None else None for p in new_right_hand]
        new_left_foot = [crop_point(p) if p is not None else None for p in new_left_foot]
        new_right_foot = [crop_point(p) if p is not None else None for p in new_right_foot]

        # Return new scaled pose
        return Pose(
            body=scaled_keypoints,
            face=new_face,
            left_hand=new_left_hand,
            right_hand=new_right_hand,
            left_foot=new_left_foot,
            right_foot=new_right_foot,
            canvas_width=self.canvas_width,
            canvas_height=self.canvas_height,
            input_age=target_age,
            input_gender=target_gender
        )

    