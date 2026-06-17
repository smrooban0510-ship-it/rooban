from flask import Flask, render_template, jsonify

import tensorflow as tf
from PIL import Image, ImageOps

import numpy as np
import requests
import cv2
from flask import Flask, render_template, jsonify, send_file

app = Flask(__name__)

# ============================================
# LOAD AI MODEL
# ============================================

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

# ============================================
# CAMERA INITIALIZATION
# ============================================


# ============================================
# GET CAMERA IMAGE
# ============================================



# ============================================
# AI DISEASE DETECTION
# ============================================

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

# ============================================
# WEATHER API
# ============================================

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


# ============================================
# HARVEST STATUS
# ============================================

def harvest_status(height):

    if float(height) > 35:

        return "Ready for Harvest"

    else:

        return "Growing"

# ============================================
# FERTILIZER RECOMMENDATION
# ============================================

def fertilizer_recommendation(
    disease,
    moisture
):

    moisture = float(moisture)

    if "LeafSpot" in disease:

        return "Copper Fungicide"

    elif "Rust" in disease:

        return "Sulfur Fungicide"

    elif moisture < 300:

        return "Organic Compost"

    else:

        return "Urea"

# ============================================
# HOME PAGE
# ============================================
# ============================================
# HOME PAGE
# ============================================

  
   
    



@app.route("/")

def home():

    return render_template("index.html")

# ============================================
# LIVE DATA
# ============================================

@app.route("/data")

def data():
    

    # GET LATEST CAMERA IMAGE FROM PI

    try:
        image = requests.get(
           "https://feof-upgrades-musical-progressive.trycloudflare.com/camera",
           timeout=5
        )


        with open("static/leaf.jpg", "wb") as f:
            f.write (image.content)
    except:
        pass

    # USER LOCATION

    location = requests.get(
        "https://ipinfo.io"
    ).json()

    #capture_image()

    # =====================================
    # 📍 USER LOCATION
    # =====================================

    location = requests.get(
        "https://ipinfo.io"
    ).json()

    city = location["city"]

    # =====================================
    # 🌱 SENSOR DATA FROM PI
    # =====================================

    sensor_data = requests.get(

        "https://feof-upgrades-musical-progressive.trycloudflare.com/sensor"

    ).json()

    moisture = sensor_data["moisture"]

    temperature = sensor_data["temperature"]

    humidity = sensor_data["humidity"]

    height = sensor_data["height"]

    # =====================================
    # 🍂 AI DISEASE DETECTION
    # =====================================

    disease = detect_disease()

    # =====================================
    # 🌦️ WEATHER
    # =====================================
    city = "sivakasi"
    weather, outside_temp = get_weather(city)
    

    if weather.lower() in [
       "rain",
       "drizzle",
       "thunderstorm"
    ]:
        rain_alert = "Yes"
    else:    
        rain_alert = "No"

    # =====================================
    # 🌾 HARVEST STATUS
    # =====================================

    harvest = harvest_status(height)

    # =====================================
    # 🧪 FERTILIZER
    # =====================================

    fertilizer = fertilizer_recommendation(

        disease,

        moisture
    )

   


    # =====================================
    # RETURN DASHBOARD DATA
    # =====================================

    return jsonify({

        "moisture": moisture,

        "temperature": temperature,

        "humidity": humidity,

        "height": height,

        "disease": disease,

        "weather": weather,

        "outside_temp": outside_temp,

        "harvest": harvest,

        "fertilizer": fertilizer,

        "city": city,

        "rain_alert": rain_alert,
    })

# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True
    )