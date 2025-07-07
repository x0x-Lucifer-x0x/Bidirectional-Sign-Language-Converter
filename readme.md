
---

# Bidirectional Sign Language Conversion Model

This repository contains a complete bidirectional system for sign language conversion:

- **Text-to-Sign Convertor** — Converts written text into animated 3D sign language gestures using landmark-based motion analysis.
- **Sign-to-Text Convertor** — Uses deep learning and computer vision to interpret hand gestures from images and predict the corresponding text in English.

The goal is to build accessible solutions that bridge communication gaps between the hearing and speech-impaired community and the general population using AI and 3D avatar technologies.


---

### 🔁 1. Text-to-Sign Converter (`Text-to-Sign-Convertor/`)

Converts **English text** into **animated 3D sign language gestures** using extracted landmarks and avatar rendering.

#### 🔹 Key Folders & Files

```
Text-to-Sign-Convertor/
├── avatar/                  ← 3D model & animation renderer
├── data/                    ← Raw landmark JSON files
├── scripts/                 ← Preprocessing & animation scripts
├── combined_avg_landmarks/ ← Smoothed landmark outputs
├── combineAllJson.py        ← JSON merger utility
├── script.cpp               ← Optional C++/Unity script
└── test.py                  ← Main inference script
```

#### 🛠️ How to Use (Text-to-Sign)

> ⚙️ Requirements: Python 3.x, `mediapipe`, `numpy`, `matplotlib`, etc.

```bash
pip install -r requirements.txt
```

1. **Prepare Data**:
   Place gesture `.json` landmark files into `data/` can be downloaded from link below: (https://www.kaggle.com/datasets/risangbaskoro/wlasl-processed).

2. **Run Preprocessing**:

   ```bash
   cd Text-to-Sign-Convertor/scripts
   python extract_landmarks.py
   python average_landmarks.py
   python convert_to_rotations.py
   ```

3. **Preview a Word**:

   ```bash
   python play_landmark_animation.py
   ```

4. **Full Conversion**:

   ```bash
   cd ..
   python test.py
   ```

   → Enter an English sentence, and the avatar will animate corresponding signs word by word.

---

### 🔁 2. Sign-to-Text Converter (`Sign-to-Text-Convertor/`)

Uses a trained CNN to classify **gesture images** and output the corresponding **English word**.

#### 🔹 Key Folders & Files

```
Sign-to-Text-Convertor/
├── dataset/            ← Training gesture images (by class)
├── test/               ← Sample inputs for testing
├── model.ipynb         ← Model training notebook
├── predict.ipynb       ← Model testing notebook
├── gesture_model.h5    ← Trained model file
├── gesture_mapping.json
├── classification_report.txt
├── confusion_matrix.png
└── prediction_results.csv
```

#### 🛠️ How to Use (Sign-to-Text)

> Recommended: Use **Jupyter Notebook** or **Google Colab**.

1. **Train the Model**

   * Place labeled gesture folders into `dataset/`
   * Run `model.ipynb` to train and save the model

2. **Test the Model**

   * Run `predict.ipynb` using images from `test/`
   * Outputs:

     * Predictions
     * Confusion matrix (`confusion_matrix.png`)
     * Performance report (`classification_report.txt`)

3. **To Add New Signs**

   * Add new labeled folders in `dataset/`
   * Retrain using `model.ipynb`

---

> ![alt text](Text-to-Sign-Convertor\visualization.png)

---


### 📚 Current Words in Dataset:

```
A, agree, answer, hello, please, eat, thank you, etc.
```

You can freely add more folders with labeled gesture images in `dataset/` to expand vocabulary.

---

## 📌 Future Work

* [ ] Host and integrate the avatar viewer (`avatar.glb`, `main.js`, `style.css`) into a working frontend interface
* [ ] Build a complete **UI application** combining both models (e.g., Flask or Streamlit)
* [ ] Add more words to both systems (especially to Sign-to-Text)
* [ ] Improve animation transitions and smoothness
* [ ] Optimize Sign-to-Text prediction for real-time webcam input
* [ ] Add webcam-based live prediction and avatar output
* [ ] Provide real-time feedback loop between modules

---

## 🤝 Contributors

This project was developed by:

* **Meet Vachhani (https://github.com/x0x-Lucifer-x0x)** 
* **Tushar Jagatap (https://github.com/TensorNaut)** 
* **Vedant Sachin Deshmukh (https://github.com/vedant4687)** 
* **Aditya Dama (https://github.com/adidama12)** 

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

