import json
import cv2
import numpy as np
import os
 
POSE_CONNECTIONS = [
    (11, 13), (13, 15), (12, 14), (14, 16), (11, 12), (23, 24),
    (11, 23), (12, 24), (23, 25), (25, 27), (24, 26), (26, 28),
    (0,1), (1,2), (2,3), (3,7), (0,4), (4,5), (5,6), (6,8), (9,10),
    (15,19), (14,18)  # Wrists to pinkies
]

HAND_CONNECTIONS = [
    (0,1), (1,2), (2,3), (3,4),
    (0,5), (5,6), (6,7), (7,8),
    (5,9), (9,10), (10,11), (11,12),
    (9,13), (13,14), (14,15), (15,16),
    (13,17), (17,18), (18,19), (19,20),
    (0,17)
]

FACE_CONNECTIONS = [
    (10, 152), (234, 454), (127, 356), (168, 8), (8, 9), (9, 10)
]

def draw_landmarks(image, landmarks, connections, color=(0,255,0)):
    for pt in landmarks:
        x, y = int(pt["x"] * 640), int(pt["y"] * 480)
        cv2.circle(image, (x, y), 2, color, -1)
    for c in connections:
        if c[0] < len(landmarks) and c[1] < len(landmarks):
            x1, y1 = int(landmarks[c[0]]["x"] * 640), int(landmarks[c[0]]["y"] * 480)
            x2, y2 = int(landmarks[c[1]]["x"] * 640), int(landmarks[c[1]]["y"] * 480)
            cv2.line(image, (x1, y1), (x2, y2), color, 1)

def play_animation(json_path):
    with open(json_path, 'r') as f:
        frames = json.load(f)

    print("▶️ Playing animation — press 'q' to quit.")
    while True:
        for frame in frames:
            canvas = np.zeros((480, 640, 3), dtype=np.uint8)

            if "pose" in frame:
                draw_landmarks(canvas, frame["pose"], POSE_CONNECTIONS, color=(0,255,0))
            if "face" in frame:
                draw_landmarks(canvas, frame["face"], FACE_CONNECTIONS, color=(255,255,0))
            if "hand_0" in frame:
                draw_landmarks(canvas, frame["hand_0"], HAND_CONNECTIONS, color=(255,0,0))
            if "hand_1" in frame:
                draw_landmarks(canvas, frame["hand_1"], HAND_CONNECTIONS, color=(0,0,255))

            cv2.imshow("Sign Animation", canvas)
            key = cv2.waitKey(50) & 0xFF  # 20 FPS
            if key == ord('q'):
                cv2.destroyAllWindows()
                print("🛑 Animation stopped.")
                return

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    print("🔍 Please select an *_average_landmarks.json file to visualize...")
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])

    if file_path:
        play_animation(file_path)
    else:
        print("❌ No file selected.")
