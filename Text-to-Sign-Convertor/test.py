







import json
import cv2
import numpy as np

# Connection mappings
POSE_CONNECTIONS = [
    (11, 13), (13, 15), (12, 14), (14, 16), (11, 12), (23, 24),
    (11, 23), (12, 24), (23, 25), (25, 27), (24, 26), (26, 28),
    (1, 2), (2, 3), (3, 7), (4, 5), (5, 6), (6, 8), (9, 10)
    # Removed: (15, 19), (14, 18)
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

# Your custom stopword list
stop_words = set([
    "mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn',
    'do', "you've", 'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are',
    "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd",
    "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then',
    'the', 'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have', 'hasn',
    'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't",
    'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn',
    "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were',
    'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't" , "," , "!" , "?" ,
])

# Draw utility
def draw_landmarks(image, landmarks, connections, color=(0,255,0)):
    for pt in landmarks:
        x, y = int(pt["x"] * 640), int(pt["y"] * 480)
        cv2.circle(image, (x, y), 3, color, -1)
    for c in connections:
        if c[0] < len(landmarks) and c[1] < len(landmarks):
            x1, y1 = int(landmarks[c[0]]["x"] * 640), int(landmarks[c[0]]["y"] * 480)
            x2, y2 = int(landmarks[c[1]]["x"] * 640), int(landmarks[c[1]]["y"] * 480)
            cv2.line(image, (x1, y1), (x2, y2), color, 1)


# Play animation from frame list
def play_frames(frame_sequence, label_sequence):
    print(" Playing animation — press 'Esc' to quit.")

    while True:
        for i, frame in enumerate(frame_sequence):
            canvas = np.zeros((480, 640, 3), dtype=np.uint8)

            # Draw pose (excluding palm joints if needed)
            if "pose" in frame:
                draw_landmarks(canvas, frame["pose"], POSE_CONNECTIONS, color=(0,255,0))

            # Draw face
            if "face" in frame:
                draw_landmarks(canvas, frame["face"], FACE_CONNECTIONS, color=(255,255,0))

            # Draw and connect left hand
            # Draw and connect left hand
            if "left_hand" in frame:
                # Adjust hand landmarks to match pose wrist position
                if "pose" in frame and len(frame["pose"]) > 15:
                    wrist_pose = frame["pose"][15]  # Left wrist from pose
                    hand_base = frame["left_hand"][0]  # Base of hand landmarks
                    
                    # Calculate offset between pose wrist and hand base
                    offset_x = wrist_pose["x"] - hand_base["x"]
                    offset_y = wrist_pose["y"] - hand_base["y"]
                    
                    # Apply offset to all hand landmarks to align with pose
                    adjusted_hand = []
                    for landmark in frame["left_hand"]:
                        adjusted_landmark = {
                            "x": landmark["x"] + offset_x,
                            "y": landmark["y"] + offset_y
                        }
                        adjusted_hand.append(adjusted_landmark)
                    
                    # Draw the adjusted hand
                    draw_landmarks(canvas, adjusted_hand, HAND_CONNECTIONS, color=(255,0,0))
                else:
                    draw_landmarks(canvas, frame["left_hand"], HAND_CONNECTIONS, color=(255,0,0))

            # Draw and connect right hand
            if "right_hand" in frame:
                # Adjust hand landmarks to match pose wrist position
                if "pose" in frame and len(frame["pose"]) > 16:
                    wrist_pose = frame["pose"][16]  # Right wrist from pose
                    hand_base = frame["right_hand"][0]  # Base of hand landmarks
                    
                    # Calculate offset between pose wrist and hand base
                    offset_x = wrist_pose["x"] - hand_base["x"]
                    offset_y = wrist_pose["y"] - hand_base["y"]
                    
                    # Apply offset to all hand landmarks to align with pose
                    adjusted_hand = []
                    for landmark in frame["right_hand"]:
                        adjusted_landmark = {
                            "x": landmark["x"] + offset_x,
                            "y": landmark["y"] + offset_y
                        }
                        adjusted_hand.append(adjusted_landmark)
                    
                    # Draw the adjusted hand
                    draw_landmarks(canvas, adjusted_hand, HAND_CONNECTIONS, color=(0,0,255))
                else:
                    draw_landmarks(canvas, frame["right_hand"], HAND_CONNECTIONS, color=(0,0,255))

            # Draw label
            cv2.putText(canvas, f"{label_sequence[i]}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Display
            cv2.imshow("Sign Animation", canvas)
            key = cv2.waitKey(40) & 0xFF  # ~12 FPS
            if key == 27:  # Esc
                print(" Animation ended by user.")
                cv2.destroyAllWindows()
                return

            
# Main execution
if __name__ == "__main__":
    with open("combined_avg_landmarks.json", "r") as f:
        data = json.load(f)

    sentence = input(" Enter a sentence: ").lower().strip()
    words = [w for w in sentence.split() if w not in stop_words]

    all_frames = []
    all_labels = []

    for word in words:
        if word in data:
            all_frames.extend(data[word])
            all_labels.extend([word] * len(data[word]))
        else:
            print(f"Fallback: spelling {word}")
            for c in word:
                if c in data:
                    all_frames.extend(data[c])
                    all_labels.extend([c] * len(data[c]))
                else:
                    print(f"No data for: {c}")

    if all_frames:
        play_frames(all_frames, all_labels)
    else:
        print("No valid landmarks to animate.")
