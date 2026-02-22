🚗 Car Damage Detection System

An AI-powered web application that detects car damage and analyzes damage severity using Deep Learning models.

📌 Project Overview

The Car Damage Detection System is a machine learning-based web application designed to:

Detect car damage from uploaded images

Identify the damage location

Predict damage severity level

Provide automated analysis through a user-friendly interface

This project demonstrates the application of Computer Vision and Deep Learning in the automobile insurance and inspection domain.

🧠 Features

📷 Upload car images for analysis

🔍 Detect damaged areas

📊 Predict damage severity

🧠 Deep learning model integration (.h5 models)

🌐 Flask-based web interface

⚡ Fast and responsive UI

🛠️ Technologies Used

Python

Flask

TensorFlow / Keras

OpenCV

HTML

CSS

Git & GitHub

📂 Project Structure
Car_Damage_Detection/
Car_Damage_Detection/
│
├── app.py
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── static/
│   ├── css/
│   ├── images/
│   └── uploads/
│
└── Car_Damage_Detection_Models/   (Not included in GitHub)
    ├── Damage_Detection.h5
    ├── car_damage_location_model.h5
    ├── car_casualty_level_model.h5
    └── other_model_files.h5
⚙️ Installation Guide
1️⃣ Clone the Repository
git clone https://github.com/hemachandrika04/car-damage-detection.git
cd car-damage-detection
2️⃣ Install Required Packages
pip install -r requirements.txt

If requirements.txt is not available, install manually:

pip install flask tensorflow keras opencv-python numpy
3️⃣ Add Trained Models

The trained .h5 model files are not included in this repository due to large file size.

Place the following model files inside:

Car_Damage_Detection_Models/

Example:

Damage_Detection.h5

car damage location model.h5

car casualty level model.h5

4️⃣ Run the Application
python app.py

Open in browser:

http://127.0.0.1:5000/
📊 How It Works

User uploads a car image

Image is preprocessed

Deep learning models analyze:

Damage presence

Damage location

Damage severity

Results are displayed on the web interface

🔐 Important Note

Model files and large assets are excluded using .gitignore to keep the repository lightweight and professional.

🚀 Future Improvements

Deploy on cloud (Render / AWS / Heroku)

Add real-time camera detection

Improve model accuracy with custom dataset

Add insurance cost estimation feature

Add database for storing damage history



