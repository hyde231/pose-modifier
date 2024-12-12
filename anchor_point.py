"""
Gravity-Assisted Support Point Determination
Overview

This algorithm identifies which body joint (from a set of key joints: ankles, knees, hips, or neck) is most likely providing the main support for a person in a static pose, given only a single 2D pose estimation from OpenPose COCO 18 keypoints. It uses both the relative positions of keypoints and a rough estimation of the center of mass (COM) to infer which joint is in contact with the ground (or providing the primary support) under gravity.
Key Concepts

    Keypoint Priority:
    The algorithm focuses on four key body regions as potential support points:
        Ankles (Feet): Highest priority, as standing humans typically support themselves on their feet.
        Knees: If ankles aren’t visible or if the person is kneeling, the knees may be the next best guess.
        Hips: In sitting or lying poses where the feet or knees are not in contact with the ground, the hips often provide support.
        Neck: In unusual or inverted poses (like a headstand), the neck or upper body region might be the main point of support.

    Vertical Alignment with Gravity:
    We assume the camera is oriented upright so that the vertical direction of the image corresponds to gravity. Consequently, the joint(s) with the largest y-value (lowest on the image) are the primary candidates for ground contact.

    Center of Mass (COM):
    To disambiguate situations where multiple joints appear at the same vertical level, we estimate a rough COM using anthropometric assumptions:
        Torso ~50% of mass
        Legs ~40% (20% each)
        Arms ~10% (lumped into the torso approximation for simplicity)

    By computing a weighted average of certain keypoints (neck, shoulders, hips, ankles), we approximate the COM’s position. In a stable pose, the COM should vertically project onto the support joint(s). When multiple joints are equally low, the one horizontally closest to the COM’s vertical line is chosen as the main support point.

Steps of the Algorithm

    Input:
    A single frame of COCO 18 keypoints from OpenPose, formatted as an array of shape (18,3): [x, y, confidence] for each keypoint.

    Filtering & Confidence Threshold:
    Discard joints with confidence below a chosen threshold (e.g., 0.1) to avoid noisy or missing detections.

    Center of Mass Calculation:
        Compute a mid-hip point from the left and right hips.
        Compute a torso center using neck, shoulders, and the mid-hip point.
        Approximate leg centers from hips and ankles.
        Combine these with assumed mass ratios to find the COM position (COM_x, COM_y).

    Identify Candidate Support Points:
        Check in order: ankles, knees, hips, then neck.
        For the first category that has visible joints, find the joint(s) with the greatest y-value (lowest in the image).

    Resolve Ties Using COM:
    If multiple joints in that category share a similar vertical level, choose the one closest to COM_x in the horizontal direction.

    Output:
    Return the name of the chosen COCO 18 keypoint. If no suitable keypoints are found, return None.

Example

For a standing person with both ankles visible at the bottom of the frame, the algorithm will:

    Identify ankles as the lowest visible joints.
    Compute the COM (likely near the midline).
    If both ankles are at nearly the same vertical level, pick the one closest to the COM_x. In a symmetrical pose, it may pick either ankle arbitrarily.

For a kneeling person where feet are not on the ground:

    Ankles might be visible but not the lowest point.
    Knees become the lowest points.
    The COM will align above the knees.
    The algorithm selects a knee as the main support point.

Robustness & Limitations

    Camera Orientation: The method assumes the camera is upright. If the camera is rotated (e.g., tilted sideways), the vertical dimension in the image no longer aligns with gravity, and the algorithm may fail.
    Occlusions & Cropping: If lower limbs are cropped out and only hips are visible at the bottom, the algorithm will choose the hips as an “optical” support point.
    Unusual Poses: For poses like headstands, if the neck region is the lowest visible joint, the algorithm will return the neck as the support point.
    Arms & Hands Not Considered: If a person is on all fours, the algorithm focuses on ankles, knees, hips, and neck only. In such cases, it will likely identify knees as the support, ignoring that hands are also providing support. This simplification is by design, as per the specified scope.

Conclusion

This gravity-assisted algorithm offers a heuristic way to guess which major body joint is supporting a static pose without 3D information or explicit floor detection. It uses vertical position, visibility, and COM alignment as cues to determine the main support point.
"""

import numpy as np

COCO_KEYPOINT_NAMES = {
    0: "Nose",
    1: "Neck",
    2: "RShoulder",
    3: "RElbow",
    4: "RWrist",
    5: "LShoulder",
    6: "LElbow",
    7: "LWrist",
    8: "RHip",
    9: "RKnee",
    10:"RAnkle",
    11:"LHip",
    12:"LKnee",
    13:"LAnkle",
    14:"REye",
    15:"LEye",
    16:"REar",
    17:"LEar"
}

# The standard COCO keypoint order used by the algorithm
COCO_KEYPOINTS_ORDER = [
    "Nose", "Neck", 
    "RShoulder", "RElbow", "RWrist", 
    "LShoulder", "LElbow", "LWrist", 
    "RHip", "RKnee", "RAnkle", 
    "LHip", "LKnee", "LAnkle", 
    "REye", "LEye", "REar", "LEar"
]

def dict_to_keypoints_array(keypoint_dict, default_conf=0.9):
    """
    Convert a dictionary of {keypoint_name: (x,y)} to a numpy array (18,3).
    Missing keypoints get confidence 0.0.
    """
    keypoints_array = np.zeros((18,3), dtype=float)
    for i, name in enumerate(COCO_KEYPOINTS_ORDER):
        if name in keypoint_dict:
            x, y = keypoint_dict[name]
            keypoints_array[i] = [x, y, default_conf]
        else:
            # Missing keypoint
            keypoints_array[i] = [0.0, 0.0, 0.0]
    return keypoints_array

def estimate_midhip(keypoints, conf_thresh=0.1):
    # RHip=8, LHip=11
    if keypoints[8,2] > conf_thresh and keypoints[11,2] > conf_thresh:
        midhip_x = (keypoints[8,0] + keypoints[11,0]) / 2.0
        midhip_y = (keypoints[8,1] + keypoints[11,1]) / 2.0
        return midhip_x, midhip_y
    return None, None

def estimate_COM(keypoints, conf_thresh=0.1):
    midhip_x, midhip_y = estimate_midhip(keypoints, conf_thresh)

    # Torso points: Neck(1), RShoulder(2), LShoulder(5)
    torso_indices = [1, 2, 5]
    torso_points = []
    for idx in torso_indices:
        if keypoints[idx,2] > conf_thresh:
            torso_points.append((keypoints[idx,0], keypoints[idx,1]))
    if midhip_x is not None:
        torso_points.append((midhip_x, midhip_y))

    if len(torso_points) == 0:
        # fallback if no torso points: use any visible point or return mean
        visible = keypoints[keypoints[:,2]>conf_thresh]
        if len(visible) == 0:
            return np.mean(keypoints[:,0]), np.mean(keypoints[:,1])
        return np.mean(visible[:,0]), np.mean(visible[:,1])

    torso_center_x = np.mean([p[0] for p in torso_points])
    torso_center_y = np.mean([p[1] for p in torso_points])

    def leg_center(hip_idx, ankle_idx):
        if keypoints[hip_idx,2]>conf_thresh and keypoints[ankle_idx,2]>conf_thresh:
            return ((keypoints[hip_idx,0] + keypoints[ankle_idx,0]) / 2.0,
                    (keypoints[hip_idx,1] + keypoints[ankle_idx,1]) / 2.0)
        elif keypoints[hip_idx,2]>conf_thresh:
            return (keypoints[hip_idx,0], keypoints[hip_idx,1])
        else:
            return (torso_center_x, torso_center_y)

    # RHip=8, RAnkle=10; LHip=11, LAnkle=13
    rleg_x, rleg_y = leg_center(8, 10)
    lleg_x, lleg_y = leg_center(11, 13)

    torso_mass = 0.5
    rleg_mass = 0.2
    lleg_mass = 0.2
    arms_mass = 0.1
    total_mass = torso_mass + rleg_mass + lleg_mass + arms_mass

    COM_x = (torso_center_x*torso_mass + rleg_x*rleg_mass + lleg_x*lleg_mass) / total_mass
    COM_y = (torso_center_y*torso_mass + rleg_y*rleg_mass + lleg_y*lleg_mass) / total_mass

    return COM_x, COM_y

def choose_main_support_with_gravity(keypoints, confidence_threshold=0.1, vertical_tolerance=5.0):
    """
    Choose a main support point from {Ankles, Knees, Hips, Neck} only if they are visible.
    If they are not in the original dictionary, they have 0 confidence and won't be chosen.
    """
    keypoints = np.asarray(keypoints)
    COM_x, COM_y = estimate_COM(keypoints, confidence_threshold)

    # Candidate groups in priority
    groups = [
        [10, 13],   # ankles: RAnkle=10, LAnkle=13
        [9, 12],    # knees: RKnee=9,  LKnee=12
        [8, 11],    # hips:  RHip=8,   LHip=11
        [1]         # neck:  Neck=1
    ]

    for group in groups:
        visible_points = [(idx, keypoints[idx,0], keypoints[idx,1]) 
                          for idx in group if keypoints[idx,2] > confidence_threshold]
        
        if len(visible_points) == 0:
            continue

        # Sort by y descending to get lowest points first
        visible_points.sort(key=lambda p: p[2], reverse=True)
        top_y = visible_points[0][2]
        # Consider all points at roughly the same vertical level
        candidates = [p for p in visible_points if abs(p[2] - top_y) <= vertical_tolerance]

        if len(candidates) == 1:
            chosen = candidates[0]
        else:
            # Pick the one closest to COM_x
            candidates.sort(key=lambda p: abs(p[1] - COM_x))
            chosen = candidates[0]

        return COCO_KEYPOINT_NAMES[chosen[0]]

    # If none found:
    return None

"""
# Example scenario:
# Given dictionary: only torso and upper body joints visible, no ankles/knees detected.
input_dict = {
    'Nose': (590.5, 445.3),
    'Neck': (614.0, 811.9),
    'RShoulder': (290.8, 834.2),
    'RElbow': (275.9, 1394.0),
    'RWrist': (300.7, 1629.3),
    'LShoulder': (937.3, 789.6),
    'LElbow': (1014.0, 1344.4),
    'LWrist': (1041.3, 1626.8),
    'RHip': (464.2, 1532.7),
    'LHip': (872.9, 1535.2),
    'REye': (508.7, 378.4),
    'LEye': (664.8, 373.5),
    'REar': (417.1, 432.9),
    'LEar': (766.3, 413.1)
}

kp_array = dict_to_keypoints_array(input_dict)
support_point = choose_main_support_with_gravity(kp_array)
print("Main support point:", support_point)
# Since ankles and knees are not provided, they have confidence 0 and won't be chosen.
# The lowest visible main joints are hips (RHip, LHip).
# COM likely aligns midline, so either "RHip" or "LHip" should be chosen, not "RAnkle".
"""