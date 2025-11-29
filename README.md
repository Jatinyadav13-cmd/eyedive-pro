# Screen Controller Through Eyes 👁️🖥️

This project enables users to control the computer screen using only their eye movements.  
It uses real-time eye tracking to move the mouse cursor and perform basic interactions without touching the keyboard or mouse.

---

## 🚀 Features
- Real-time eye detection and tracking using webcam  
- Cursor movement based on pupil direction  
- Blink-based click system  
- Works without external hardware  
- Helpful for physically disabled users  
- Can be integrated into AI-based assistants  

---

## 🧠 Tech Stack / Libraries
- Python  
- :contentReference[oaicite:0]{index=0} – for image processing  
- :contentReference[oaicite:1]{index=1} – for facial landmark detection  
- :contentReference[oaicite:2]{index=2} – for array operations  
- :contentReference[oaicite:3]{index=3} – for mouse control  

---





screen-controller-eyes/
│
├── main.py # main eye-tracking + cursor control code
├── eye_utils.py # helper functions for blink, gaze, landmark detection
├── requirements.txt # list of required libraries
├── models/ # facial landmark models
│ └── shape_predictor_68_face_landmarks.dat
└── README.md # project documentation



---

## ⚙️ How It Works

1. Webcam captures your face  
2. Facial landmarks around the eyes are detected  
3. Pupil movement (left, right, up, down) is measured  
4. Cursor moves based on pupil direction  
5. Blink or long blink → converted into click action  
6. Smooth cursor movement using filtered gaze points  

---

## ▶️ How to Run

### **1. Clone the repository**


git clone https://github.com/yourusername/screen-controller-eyes.git cd screen-controller-eyes

### **2. Install dependencies**
pip install -r requirements.txt

### **3. Download facial landmark model**
Place it inside `/models` folder:  
`shape_predictor_68_face_landmarks.dat`

### **4. Run the project**
python main.py




---

## 📌 Use Cases
- Hands-free screen control  
- Accessibility for disabled users  
- Robotics and automation  
- Smart AI assistants  
- Research and computer vision projects  

---

## 🛠️ Future Improvements
- Better accuracy with deep learning  
- Click gestures using both eyes  
- On-screen keyboard  
- Calibrated movement for gaming / productivity  

---

## 🧑‍💻 Author
**Jatin**  
Final year AI/ML Engineer  
Always learning. Always building.







## 📂 Project Structure

