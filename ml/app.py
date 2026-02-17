from flask import Flask, request, jsonify
import requests
from datetime import datetime
from scheduler.event_scanner import start_scheduler
from clarity.predict_visibility import predict_visibility
from utils.space_api import get_cloud_cover, get_iss_pass, get_moon_phase, get_light_pollution
from scheduler.event_scanner import TODAY_EVENTS
from explainer.gemini_explainer import generate_celestial_explanation
import os
app = Flask(__name__)

# ==========================
# CONFIG
# ==========================



# ==========================
# ROUTES
# ==========================

@app.route("/")
def home():
    return "Visibility ML API Running"


@app.route("/auto-visibility", methods=["POST"])
def auto_visibility():

    data = request.json

    lat = data["lat"]
    lon = data["lon"]
    city = data["city"]

    # ===== FETCH LIVE FEATURES =====
    cloud_cover = get_cloud_cover(lat, lon)

    altitude, duration = get_iss_pass(lat, lon)

    moon_phase = get_moon_phase()

    light_pollution = get_light_pollution(city)

    hour = datetime.now().hour

    features = {
        "cloud_cover": cloud_cover,
        "altitude": altitude,
        "duration": duration,
        "moon_phase": moon_phase,
        "light_pollution": light_pollution,
        "hour": hour
    }

    # ===== ML PREDICTION =====
    result = predict_visibility(features)

    return jsonify({
        "features_used": features,
        "visibility_level": result
    })

@app.route("/today-events", methods=["GET"])
def today_events():
    return jsonify(TODAY_EVENTS)

@app.route("/explain-event", methods=["POST"])
def explain_event():

    data = request.json

    raw_text = data["raw_text"]
    event_name = data["event_name"]

    result = generate_celestial_explanation(raw_text, event_name)

    return jsonify({
        "explanation": result
    })
# ==========================
# RUN SERVER
start_scheduler()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
