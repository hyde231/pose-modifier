from dataclasses import dataclass, field
from typing import List, Dict, Optional
import cv2
import os
import numpy as np

from Pose import Pose 

from visualization import build_pose_graph, draw_pose_with_graph, create_graphs_for_poses

class OpenPoseError(Exception):
    pass

@dataclass
class OpenPose:
    """
    Represents the entire OpenPose JSON data structure, handling multiple poses and canvas dimensions.
    """
    people: List[Pose] = field(default_factory=list)
    canvas_width: int = 0
    canvas_height: int = 0

    def to_json(self) -> List[Dict]:
        """
        Converts the OpenPose object to JSON format compatible with OpenPose output.
        Returns an array with a single dictionary, as per OpenPose's JSON structure.
        """
        return [{
            "people": [pose.to_json() for pose in self.people],
            "canvas_width": self.canvas_width,
            "canvas_height": self.canvas_height
        }]

    @classmethod
    def from_json(cls, data: Dict) -> "OpenPose":
        """
        Creates an OpenPose object from JSON data.
        """
        canvas_width=data.get("canvas_width", 0)
        canvas_height=data.get("canvas_height", 0)

        return cls(
            people=[Pose.from_json(person,canvas_width,canvas_height) for person in data.get("people", [])],
            canvas_width=canvas_width,
            canvas_height=canvas_height
        )

    @classmethod
    def load(cls, file_path: str) -> "OpenPose":
        import json

        def validate_and_process_data(data):
            """
            Validates and processes the loaded JSON data.
            Ensures all keypoints are iterable and not None.
            """
            if not isinstance(data, dict) or "people" not in data:
                raise OpenPoseError(f"The data format is invalid: {data}")

            for person in data.get("people", []):
                person["pose_keypoints_2d"] = person.get("pose_keypoints_2d") or []
                person["face_keypoints_2d"] = person.get("face_keypoints_2d") or []
                person["hand_left_keypoints_2d"] = person.get("hand_left_keypoints_2d") or []
                person["hand_right_keypoints_2d"] = person.get("hand_right_keypoints_2d") or []

            return data

        try:
            with open(file_path, "r") as file:
                raw_data = json.load(file)

            # Handle case where top-level JSON is a list
            if isinstance(raw_data, list) and len(raw_data) > 0:
                raw_data = raw_data[0]

            # Validate and process the data
            processed_data = validate_and_process_data(raw_data)

            # Initialize the object using from_json
            return cls.from_json(processed_data)

        except FileNotFoundError:
            raise OpenPoseError(f"The file at {file_path} was not found.")
        except json.JSONDecodeError:
            raise OpenPoseError(f"The file at {file_path} contains invalid JSON.")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while loading the file: {e}")


    def save(self, file_path: str) -> None:
        import json
        try:
            with open(file_path, "w") as file:
                json.dump(self.to_json(), file, indent=4)
        except PermissionError:
            raise OpenPoseError(f"Permission denied when trying to save to {file_path}.")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while saving the file: {e}")


    def merge(self, other: "OpenPose") -> None:
        """
        Merges another OpenPose object into this one.
        """
        self.people.extend(other.people)
        self.canvas_width = max(self.canvas_width, other.canvas_width)
        self.canvas_height = max(self.canvas_height, other.canvas_height)

    def get_pose(self, index: int) -> Optional[Pose]:
        """
        Retrieves a Pose object by its index.
        """
        return self.people[index] if 0 <= index < len(self.people) else None

    def add_pose(self, pose: Pose) -> None:
        """
        Adds a Pose object to the OpenPose data.
        """
        self.people.append(pose)

    def remove_pose(self, index: int) -> None:
        """
        Removes a Pose object by its index.
        """
        if 0 <= index < len(self.people):
            del self.people[index]

    def keep_pose(self, index: int) -> None:
        """
        Keeps only the Pose object at the specified index, removing all others.
        """
        if 0 <= index < len(self.people):
            self.people = [self.people[index]]

    def scale_pose(self, index: int, target_gender: str, target_age: int) -> None:
        """
        Scales a Pose object at the specified index to a new gender and age.
        """
        if 0 <= index < len(self.people):
            pose = self.people[index]
            self.people[index] = pose.scale(target_gender, target_age)

    def guess_age(self, index: int) -> Optional[int]:
        """
        Guesses the age of the person at the specified index.
        """
        if 0 <= index < len(self.people):
            return self.people[index].guess_age()
        return None

    def guess_gender(self, index: int) -> Optional[str]:
        """
        Guesses the gender of the person at the specified index.
        """
        if 0 <= index < len(self.people):
            return self.people[index].guess_gender()
        return None

    def draw(self) -> np.ndarray:
        """
        Renders all poses on a canvas and returns the resulting image.

        Returns:
            np.ndarray: The canvas with all poses drawn.
        """
        import numpy as np

        # Create a blank canvas
        canvas = np.zeros((self.canvas_height, self.canvas_width, 3), dtype=np.uint8)

        # Build graphs for all poses
        graphs = create_graphs_for_poses(self.people)

        # Draw each pose with its corresponding graph
        for pose, graph in zip(self.people, graphs):
            draw_pose_with_graph(canvas, pose, graph)

        return canvas

    def save_as_image(self, file_path: str) -> None:
        """
        Saves the rendered image of the OpenPose object to a file.

        Parameters:
            file_path (str): The file path to save the image, including the extension (e.g., 'output.png').
        """
        # Draw the image
        canvas = self.draw()

        success = cv2.imwrite(file_path, canvas)
        if not success:
            raise RuntimeError(f"Failed to save image to {file_path}.")

        """
        # Save the image
        try:
            success = cv2.imwrite(file_path, canvas)
            if not success:
                raise OpenPoseError(f"Failed to save image to {file_path}.")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while saving the image: {e}")
        """