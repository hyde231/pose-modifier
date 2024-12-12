from typing import List
import cv2
import numpy as np
import networkx as nx
import logging

from Pose import Pose

logging.basicConfig(level=logging.WARNING)

# Define color map for body parts
colors = {
    "Nose": (204, 51, 255),
    "Neck": (102, 204, 255),
    "RShoulder": (255, 128, 0),
    "RElbow": (255, 204, 51),
    "RWrist": (255, 255, 102),
    "LShoulder": (0, 255, 128),
    "LElbow": (51, 255, 204),
    "LWrist": (102, 255, 255),
    "RHip": (153, 153, 255),
    "RKnee": (102, 51, 204),
    "RAnkle": (51, 0, 153),
    "LHip": (153, 153, 255),
    "LKnee": (102, 51, 204),
    "LAnkle": (51, 0, 153),
    "REye": (255, 51, 102),
    "LEye": (255, 51, 102),
    "REar": (255, 102, 153),
    "LEar": (255, 102, 153),
}

# Additional color maps for other regions
region_colors = {
    "face": (0, 255, 0),
    "right_hand": (0, 0, 255),
    "left_hand": (0, 0, 255),
    "right_foot": (255, 255, 0),
    "left_foot": (255, 255, 0),
}

def build_pose_graph(pose: Pose) -> nx.Graph:
    """
    Builds a graph representation of a Pose object.

    Parameters:
        pose (Pose): A Pose object containing body keypoints.

    Returns:
        nx.Graph: A NetworkX graph representing the pose.
    """
    G = nx.Graph()

    # Define edges based on COCO keypoints
    edges = [
        ("Nose", "Neck"), ("Neck", "RShoulder"), ("RShoulder", "RElbow"),
        ("RElbow", "RWrist"), ("Neck", "LShoulder"), ("LShoulder", "LElbow"),
        ("LElbow", "LWrist"), ("Neck", "RHip"), ("RHip", "RKnee"),
        ("RKnee", "RAnkle"), ("Neck", "LHip"), ("LHip", "LKnee"),
        ("LKnee", "LAnkle"), ("Nose", "REye"), ("REye", "REar"),
        ("Nose", "LEye"), ("LEye", "LEar")
    ]

    # Add nodes for all valid keypoints
    for keypoint, coords in pose.body.items():
        if coords is not None and not np.any(np.isnan(coords)):  # Ensure keypoint is valid
            G.add_node(keypoint, pos=coords)
        else:
            logging.warning(f"Invalid or missing keypoint: {keypoint} with coords: {coords}")

    # Add edges only if both keypoints are present
    for start, end in edges:
        if start in G and end in G:
            G.add_edge(start, end)
        else:
            missing = [k for k in [start, end] if k not in G]
            logging.warning(f"Missing keypoint(s) {missing} for edge ({start}, {end}).")

    return G

def create_graphs_for_poses(poses: List[Pose]) -> List[nx.Graph]:
    """
    Creates a list of graphs for multiple poses.

    Parameters:
        poses (List[Pose]): A list of Pose objects.

    Returns:
        List[nx.Graph]: A list of graphs, one for each Pose.
    """
    graphs = []
    for pose in poses:
        graph = build_pose_graph(pose)
        graphs.append(graph)
    return graphs

def draw_pose_with_graph(canvas: np.ndarray, pose: Pose, graph: nx.Graph) -> None:
    """
    Draws a pose on the given canvas using a graph representation.

    Parameters:
        canvas (np.ndarray): The canvas to draw on.
        pose (Pose): The Pose object containing keypoints.
        graph (nx.Graph): The graph representation of the pose.
    """
    # Draw edges (connections between joints)
    for start, end in graph.edges:
        if start in graph.nodes and end in graph.nodes:
            start_pos = graph.nodes[start]["pos"]
            end_pos = graph.nodes[end]["pos"]
            start_color = colors.get(start, (255, 255, 255))  # Default to white
            end_color = colors.get(end, (255, 255, 255))      # Default to white

            # Draw the edge
            cv2.line(
                canvas,
                (int(start_pos[0]), int(start_pos[1])),
                (int(end_pos[0]), int(end_pos[1])),
                color=tuple(np.mean([start_color, end_color], axis=0).astype(int).tolist()),  # Fix
                thickness=2
            )
        else:
            logging.warning(f"Skipping edge ({start}, {end}) with invalid positions: {start_pos}, {end_pos}")

    # Draw nodes (keypoints)
    for node, data in graph.nodes(data=True):
        pos = data.get("pos")
        if pos is not None and not np.any(np.isnan(pos)):  # Check for NaN
            color = colors.get(node, (255, 255, 255))  # Default to white
            cv2.circle(canvas, (int(pos[0]), int(pos[1])), radius=4, color=color, thickness=-1)
        else:
            logging.warning(f"Skipping node {node} with invalid position: {pos}")

    # Draw face, hand, and foot points using region colors
    for region, points in [
        ("face", pose.face),
        ("right_hand", pose.right_hand),
        ("left_hand", pose.left_hand),
        ("right_foot", pose.right_foot),
        ("left_foot", pose.left_foot)
    ]:
        color = region_colors[region]
        for point in points:
            if point:
                cv2.circle(canvas, (int(point[0]), int(point[1])), radius=2, color=color, thickness=-1)