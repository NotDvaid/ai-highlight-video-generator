import cv2
import numpy as np
from typing import List


class VideoFeatureExtractor:
    """Extract real features from video segments for the AI highlight model."""

    @staticmethod
    def compute_motion_score(frames: List[str]) -> float:
        if len(frames) < 2:
            return 0.0
        prev = cv2.imread(frames[0], cv2.IMREAD_GRAYSCALE)
        if prev is None:
            return 0.0
        prev = cv2.resize(prev, (320, 240))
        total_diff = 0.0
        count = 0
        for frame_path in frames[1:]:
            curr = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
            if curr is None:
                continue
            curr = cv2.resize(curr, (320, 240))
            diff = cv2.absdiff(prev, curr)
            total_diff += np.mean(diff) / 255.0
            prev = curr
            count += 1
        return total_diff / max(count, 1)

    @staticmethod
    def compute_brightness(frames: List[str]) -> float:
        if not frames:
            return 0.0
        total = 0.0
        count = 0
        for frame_path in frames:
            img = cv2.imread(frame_path)
            if img is None:
                continue
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            total += np.mean(hsv[:, :, 2]) / 255.0
            count += 1
        return total / max(count, 1)

    @staticmethod
    def compute_colorfulness(frames: List[str]) -> float:
        if not frames:
            return 0.0
        total = 0.0
        count = 0
        for frame_path in frames:
            img = cv2.imread(frame_path)
            if img is None:
                continue
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            total += np.mean(hsv[:, :, 1]) / 255.0
            count += 1
        return total / max(count, 1)

    @staticmethod
    def compute_sharpness(frames: List[str]) -> float:
        if not frames:
            return 0.0
        total = 0.0
        count = 0
        for frame_path in frames:
            img = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = cv2.resize(img, (320, 240))
            laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
            total += min(laplacian_var / 500.0, 1.0)
            count += 1
        return total / max(count, 1)

    @classmethod
    def extract_features_from_clip(video_path: str, start: float, end: float):
"""Extract real features from a video segment."""
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)

    frames = []
    brightnesses = []

    while cap.get(cv2.CAP_PROP_POS_MSEC) < end * 1000:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        # Brightness: average pixel intensity
        brightnesses.append(np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)))

    cap.release()

    if len(frames) < 2:
        return [0.0, 0.0, 0.0]

    # Motion: average frame-to-frame difference
    diffs = []
    for i in range(1, len(frames)):
        diff = cv2.absdiff(frames[i], frames[i-1])
        diffs.append(np.mean(diff))
    motion = np.mean(diffs) / 255.0  # normalize to 0-1

    # Brightness: normalized average
    brightness = np.mean(brightnesses) / 255.0

    # Sharpness: Laplacian variance (measures focus/detail)
    sharpness = np.mean([cv2.Laplacian(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var() for f in frames])
    sharpness = min(sharpness / 500.0, 1.0)  # normalize

    return [motion, brightness, sharpness]
    

