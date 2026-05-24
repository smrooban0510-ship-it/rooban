from flask import Flask, render_template, jsonify

import tensorflow as tf
from PIL import Image, ImageOps

import numpy as np
import random
import requests
import cv2

app = Flask(__name__)

# =====================================================
# 🤖 LOAD TFLITE MODEL
# =====================================================

interpreter = tf.lite.Interpreter(
    model_path="model/model.tflite"
)

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()

output_details = interpreter.get_output_details()

class_names = open(
    "model/labels.txt",
    "r"
).readlines()

# =====================================================
# 📸 CAMERA CAPTURE
# =====================================================

def capture_image():

    cam = cv2.VideoCapture(0)

    ret, frame = cam.read()

    if ret:

        cv2.imwrite(
            "static/leaf.jpg",
            frame
        )

    cam.release()

# =====================================================
# 🍂 AI DISEASE DETECTION
# =====================================================

def detect_disease():

    image = Image.open(
        "static/leaf.jpg"
    ).convert("RGB")

    size = (224,224)

    image = ImageOps.fit(
        image,
        size
    )

    image_array = np.asarray(image)

    normalized_image_array = (
        image_array.astype(np.float32) / 127.5
    ) - 1

    input_data = np.expand_dims(
        normalized_image_array,
        axis=0
    )

    interpreter.set_tensor(
        input_details[0]['index'],
        input_data
    )

    interpreter.invoke()

    output_data = interpreter.get_tensor(
        output_details[0]['index']
    )

    index = np.argmax(output_data)

    disease = class_names[index][2:].strip()

    return disease

# =====================================================
# 🌱 SOIL MOISTURE
# =====================================================

def get_moisture():

    return random.randint(200,500)

# =====================================================
# 🌡️ TEMPERATURE
# =====================================================

def get_temperature():

    return random.randint(20,40)

# =====================================================
# 📏 PLANT HEIGHT
# =====================================================

def get_height():

    return random.randint(10,45)

# =====================================================
# 🌦️ WEATHER
# =====================================================

def get_weather(city):

    API_KEY = "0b0711cd388ad4bb2fca27a82a945e62"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    data = requests.get(url).json()

    if "weather" in data:

        weather = data["weather"][0]["main"]

        outside_temp = data["main"]["temp"]

    else:

        weather = "Clouds"

        outside_temp = 30

    return weather, outside_temp

# =====================================================
# 🌾 HARVEST STATUS
# =====================================================

def harvest_status(height):

    if height > 35:

        return "Ready"

    else:

        return "Growing"

# =====================================================
# 🧪 FERTILIZER RECOMMENDATION
# =====================================================

def fertilizer_recommendation(
    disease,
    moisture
):

    if "LeafSpot" in disease:

        return "Copper Fungicide"

    elif "Rust" in disease:

        return "Sulfur Fungicide"

    elif moisture < 250:

        return "Organic Compost"

    else:

        return "Urea"

# =====================================================
# 🏠 HOME PAGE
# =====================================================

@app.route("/")
def home():

    return render_template("index.html")

# =====================================================
# 📊 LIVE DATA
# =====================================================

@app.route("/data")
def data():

    # 📸 Capture leaf image
    capture_image()

    # 📍 Detect city
    location = requests.get(
        "https://ipinfo.io"
    ).json()

    city = location["city"]

    # 🌱 Sensor values
    moisture = get_moisture()

    temperature = get_temperature()

    height = get_height()

    # 🍂 AI Disease Detection
    disease = detect_disease()

    # 🌦️ Weather
    weather, outside_temp = get_weather(city)

    # 🌾 Harvest
    harvest = harvest_status(height)

    # 🧪 Fertilizer
    fertilizer = fertilizer_recommendation(
        disease,
        moisture
    )

    return jsonify({

        "moisture": moisture,

        "temperature": temperature,

        "height": height,

        "disease": disease,

        "weather": weather,

        "outside_temp": outside_temp,

        "harvest": harvest,

        "fertilizer": fertilizer,

        "city": city
    })

# =====================================================
# ▶️ RUN SERVER
# =====================================================

if __name__ == "__main__":

    app.run(debug=True)