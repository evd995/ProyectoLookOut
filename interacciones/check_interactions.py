"""
Check if two people are interacting/looking at each other
"""

import numpy as np
import cv2

# Import libraries for face recognition
from ..head_pose_estimation.pose_estimator import PoseEstimator
from ..head_pose_estimation.mark_detector import FaceDetector, MarkDetector


class InteractionDetector:
    """Detect interactions according to PoseEstimator"""

    def __init__(self, img_size=(480, 640)):
        self.size = img_size
        self.pose_estimator = PoseEstimator()
        self.face_detector = FaceDetector()
        self.mark_detector = MarkDetector()

    def check_interaction(self, points_2d, other_points_2d):
        """
        Recieves 2d points of target and compares it with other_points_2d

        Returns an array of coeficients of interaction for each subject in other_points_2d
        """
        pass
