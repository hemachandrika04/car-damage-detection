from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array

app = Flask(__name__)

# Define paths for models
MODEL_PATHS = {
    "car_detection": r"C:\Users\jalla\Downloads\Car_Damage_Detection_Models\model1.h5",
    "damage_detection": r"C:\Users\jalla\Downloads\Car_Damage_Detection_Models\Damage_Detection.h5",
    "location_detection": r"C:\Users\jalla\Downloads\Car_Damage_Detection_Models\car damage location model.h5",
    "severity_detection": r"C:\Users\jalla\Downloads\Car_Damage_Detection_Models\car casuality level model.h5"
}

# Load models with error handling
models = {}
for key, path in MODEL_PATHS.items():
    if os.path.exists(path):
        print(f"✅ Loading model: {key} from {path}")
        models[key] = load_model(path)
    else:
        print(f"❌ Model file not found: {path}")
        models[key] = None  # Prevent crashes if a model is missing

# Function to preprocess images dynamically based on model input shape
def preprocess_image(img_path, target_size):
    """Loads and preprocesses an image based on target size."""
    if not os.path.exists(img_path):
        print(f"❌ Error: Image not found at {img_path}")
        return None

    img = load_img(img_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize to [0,1]
    
    print(f"📌 Image shape after preprocessing: {img_array.shape}")
    return img_array

# Pipeline 1: Car Detection
def is_car(img_path):
    """Checks if the image contains a car."""
    print("\n🔹 Step 1: Checking if the image contains a car...")
    model = models["car_detection"]
    
    if model is None:
        print("❌ Car detection model not available.")
        return False
    
    img_array = preprocess_image(img_path, model.input_shape[1:3])
    if img_array is None:
        return False

    prediction = model.predict(img_array)
    print(f"📌 Car Model Raw Prediction: {prediction}")
    
    return prediction[0][0] >= 0.5  # Assuming Sigmoid activation

# Pipeline 2: Damage Detection (Updated with Dynamic Resizing)
def is_damaged(img_path):
    """Determines if the car is damaged or not."""
    print("\n🔹 Step 2: Checking if the car is damaged...")
    model = models["damage_detection"]
    
    if model is None:
        print("❌ Damage detection model not available.")
        return False

    # Get correct input size dynamically
    target_size = model.input_shape[1:3]  
    img_array = preprocess_image(img_path, target_size)
    if img_array is None:
        return False

    prediction = model.predict(img_array)
    print(f"📌 Damage Model Raw Prediction: {prediction}")

    labels = ['damaged', 'not_damaged']
    predicted_class_index = np.argmax(prediction)  
    predicted_class_label = labels[predicted_class_index]

    print(f"✅ Predicted class index: {predicted_class_index}")
    print(f"✅ Predicted class label: {predicted_class_label}")

    return predicted_class_label == "damaged"

# Pipeline 3: Damage Location Detection
def get_damage_location(img_path):
    """Determines the location of the damage."""
    print("\n🔹 Step 3: Identifying the damage location...")
    model = models["location_detection"]
    
    if model is None:
        print("❌ Damage location model not available.")
        return None

    img_array = preprocess_image(img_path, model.input_shape[1:3])
    if img_array is None:
        return None

    prediction = model.predict(img_array)
    print(f"📌 Location Model Raw Prediction: {prediction}")

    labels = {0: 'Front', 1: 'Rear', 2: 'Side'}
    return labels.get(np.argmax(prediction), "Unknown")

# Pipeline 4: Damage Severity Detection
def get_damage_severity(img_path):
    """Determines the severity of the damage."""
    print("\n🔹 Step 4: Estimating damage severity...")
    model = models["severity_detection"]
    
    if model is None:
        print("❌ Severity detection model not available.")
        return None

    img_array = preprocess_image(img_path, model.input_shape[1:3])
    if img_array is None:
        return None

    prediction = model.predict(img_array)
    print(f"📌 Severity Model Raw Prediction: {prediction}")

    labels = {0: 'Minor', 1: 'Moderate', 2: 'Severe'}
    return labels.get(np.argmax(prediction), "Unknown")

# Full Pipeline
def analyze_car_damage(img_path):
    """Runs full pipeline to detect car, damage, location, and severity."""
    results = {
        "car": "No",
        "damaged": "No",
        "severity": "N/A",
        "location": "N/A"
    }

    if not is_car(img_path):
        print("\n❌ The image is NOT a car. Please try again with a different image.")
        return results

    results["car"] = "Yes"
    print("\n✅ The image contains a car. Proceeding to damage detection...")

    if not is_damaged(img_path):
        print("\n✅ The car is NOT damaged.")
        return results

    results["damaged"] = "Yes"
    print("\n✅ The car is damaged. Analyzing further...")

    location = get_damage_location(img_path)
    severity = get_damage_severity(img_path)

    if location:
        results["location"] = location
    if severity:
        results["severity"] = severity

    return results

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('static', 'uploads', filename)
        file.save(filepath)
        
        results = analyze_car_damage(filepath)
        return render_template('index.html', results=results, image_url=filepath)

if __name__ == "__main__":
    app.run(debug=True)