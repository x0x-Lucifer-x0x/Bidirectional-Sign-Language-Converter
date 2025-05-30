# import os
# import json

# base_path = "data"  # path to your data folder
# output_file = "combined_avg_landmarks.json"

# combined = {}

# # Traverse each word folder
# for word in os.listdir(base_path):
#     word_folder = os.path.join(base_path, word)
#     if not os.path.isdir(word_folder):
#         continue

#     rotation_file = os.path.join(word_folder, f"{word}_average_landmarks.json")
#     if not os.path.exists(rotation_file):
#         print(f"⚠️ Missing: {rotation_file}")
#         continue

#     with open(rotation_file, "r") as f:
#         try:
#             rotations = json.load(f)
#             combined[word] = rotations
#         except Exception as e:
#             print(f"❌ Error reading {rotation_file}: {e}")

# # Save final merged JSON
# with open(output_file, "w") as f:
#     json.dump(combined, f, indent=2)

# print(f"✅ Combined rotation file created → {output_file}")
 


import os
import json

base_path = "data"  # path to your data folder
output_file = "combined_avg_landmarks.json"

# List of allowed words
allowed_words = {
    'he', 'how', 'go', 'come', 'eat', 'drink', 'help', 'know', 'give', 'father',
    'brother', 'baby', 'boy', 'before', 'book', 'bed', 'bread', 'banana', 'black',
    'blue', 'bad', 'angry', 'apple', 'car', 'chair', 'cold', 'candy', 'computer',
    'cousin', 'coffee', 'day', 'different', 'door', 'after', 'good', 'girl', 'home',
    'house', 'hot', 'happy', 'i', 'eat', 'know', 'help', 'go', 'come', 'drink'
}


combined = {}

# Traverse each word folder
for word in os.listdir(base_path):
    if word not in allowed_words:
        continue

    word_folder = os.path.join(base_path, word)
    if not os.path.isdir(word_folder):
        continue

    rotation_file = os.path.join(word_folder, f"{word}_average_landmarks.json")
    if not os.path.exists(rotation_file):
        print(f"⚠️ Missing: {rotation_file}")
        continue

    with open(rotation_file, "r") as f:
        try:
            rotations = json.load(f)
            combined[word] = rotations
        except Exception as e:
            print(f"❌ Error reading {rotation_file}: {e}")

# Save final merged JSON
with open(output_file, "w") as f:
    json.dump(combined, f, indent=2)

print(f"✅ Combined rotation file created → {output_file}")
