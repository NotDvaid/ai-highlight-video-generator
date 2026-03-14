# cat > feature_extraction.py << 'EOF'
import cv2
import numpy as np


def extract_features_from_clip(video_path, start, end):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)
    frames = []
    brightnesses = []
    while cap.get(cv2.CAP_PROP_POS_MSEC) < end * 1000:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        brightnesses.append(np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)))
    cap.release()
    if len(frames) < 2:
        return [0.0, 0.0, 0.0, 0.0]
    diffs = []
    for i in range(1, len(frames)):
        diff = cv2.absdiff(frames[i], frames[i-1])
        diffs.append(np.mean(diff))
    motion = np.mean(diffs) / 255.0
    brightness = np.mean(brightnesses) / 255.0
    sharpness = np.mean([cv2.Laplacian(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var() for f in frames])
    sharpness = min(sharpness / 500.0, 1.0)
    contrast = np.mean([np.std(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)) for f in frames])
    contrast = min(contrast / 128.0, 1.0)
    return [motion, brightness, sharpness, contrast]
