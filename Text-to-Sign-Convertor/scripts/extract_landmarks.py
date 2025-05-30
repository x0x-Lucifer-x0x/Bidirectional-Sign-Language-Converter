#V3 with 543+ points

import cv2
import mediapipe as mp
import json
import os
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

mp_holistic = mp.solutions.holistic

# Settings (turn OFF specific parts if needed for performance)
USE_POSE = True
USE_HANDS = True
USE_FACE = True

# Init Holistic model
holistic = mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=2,
    smooth_landmarks=True,
    enable_segmentation=False,
    refine_face_landmarks=True,  # Get iris + lips + detailed mesh
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def extract_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(rgb)

        frame_data = {}

        # Pose landmarks
        if USE_POSE and results.pose_landmarks:
            frame_data["pose"] = [
                {"x": lm.x, "y": lm.y, "z": lm.z, "v": lm.visibility}
                for lm in results.pose_landmarks.landmark
            ]

        # Left hand
        if USE_HANDS and results.left_hand_landmarks:
            frame_data["left_hand"] = [
                {"x": lm.x, "y": lm.y, "z": lm.z}
                for lm in results.left_hand_landmarks.landmark
            ]

        # Right hand
        if USE_HANDS and results.right_hand_landmarks:
            frame_data["right_hand"] = [
                {"x": lm.x, "y": lm.y, "z": lm.z}
                for lm in results.right_hand_landmarks.landmark
            ]

        # Face mesh
        if USE_FACE and results.face_landmarks:
            frame_data["face"] = [
                {"x": lm.x, "y": lm.y, "z": lm.z}
                for lm in results.face_landmarks.landmark
            ]

        frames.append(frame_data)

    cap.release()
    return frames




base_path = "../data"
start_from = "health"

def process_video(args):
    word_folder, video = args
    full_path = os.path.join(word_folder, video)
    out_path = os.path.join(word_folder, video.replace(".mp4", "_landmarks.json"))

    print(f"Processing: {full_path}")
    landmarks = extract_from_video(full_path)
    with open(out_path, "w") as f:
        json.dump(landmarks, f)

if __name__ == "__main__":
    tasks = []
    start_collecting = False

    for word_entry in sorted(os.scandir(base_path), key=lambda x: x.name):
        if word_entry.is_dir():
            if word_entry.name == start_from:
                start_collecting = True
            if not start_collecting:
                continue

            for video_entry in sorted(os.scandir(word_entry.path), key=lambda x: x.name):
                if video_entry.name.endswith(".mp4"):
                    tasks.append((word_entry.path, video_entry.name))

    with ProcessPoolExecutor() as executor:
        list(tqdm(executor.map(process_video, tasks), total=len(tasks), desc="Processing videos"))


print("✅ Full landmark extraction completed (pose, hands, face).")
    