from apscheduler.schedulers.background import BackgroundScheduler
from clarity.predict_visibility import predict_visibility
from utils.space_api import (
    get_cloud_cover,
    get_iss_pass,
    get_moon_phase,
    get_light_pollution
)
from datetime import datetime
from explainer.gemini_explainer import generate_celestial_explanation

TODAY_EVENTS = []


def scan_events():

    print("Scanning DAILY IMPORTANT celestial events...")

    lat = 19.07
    lon = 72.87
    city = "Mumbai"

    # =========================
    # DAILY IMPORTANT EVENTS LIST
    # (Later this will come from APIs)
    # =========================
    important_events = [
        {
            "name": "ISS Flyover",
            "description": "The International Space Station will pass over the sky and reach a high elevation."
        },
        {
            "name": "Meteor Activity",
            "description": "Small meteors may be visible as quick streaks of light during the night."
        },
        {
            "name": "Planet Visibility",
            "description": "A bright planet will be visible near the western horizon after sunset."
        }
    ]

    TODAY_EVENTS.clear()

    # =========================
    # LOOP THROUGH DAILY EVENTS
    # =========================
    for event_data in important_events:

        print(f"Processing event: {event_data['name']}")

        # ---- Common environment data
        cloud_cover = get_cloud_cover(lat, lon)
        moon_phase = get_moon_phase()
        light_pollution = get_light_pollution(city)
        hour = datetime.now().hour

        # =========================
        # EVENT-TYPE AWARE FEATURES
        # =========================
        if event_data["name"] == "ISS Flyover":

            altitude, duration = get_iss_pass(lat, lon)

        elif event_data["name"] == "Meteor Activity":

            # Meteors usually appear high and fast
            altitude = 70
            duration = 8

        elif event_data["name"] == "Planet Visibility":

            # Planets stay longer but slightly lower
            altitude = 55
            duration = 6

        else:
            altitude = 40
            duration = 3

        features = {
            "cloud_cover": cloud_cover,
            "altitude": altitude,
            "duration": duration,
            "moon_phase": moon_phase,
            "light_pollution": light_pollution,
            "hour": hour
        }

        # ---- Visibility ML
        visibility = predict_visibility(features)
        print(f"{event_data['name']} Visibility:", visibility)

        # ---- Gemini Explainer
        try:
            ai_explanation = generate_celestial_explanation(
                event_data["description"],
                event_data["name"]
            )

            if not isinstance(ai_explanation, dict):
                raise ValueError("Gemini output not structured")

        except Exception as e:
            print("Gemini explainer failed:", e)

            ai_explanation = {
                "title": event_data["name"],
                "simple_explanation": "A celestial event will be visible in the sky.",
                "difficulty": "Moderate",
                "random_facts": [
                    "Space is vast and full of moving objects.",
                    "Astronomy helps us understand our universe.",
                    "Clear skies improve visibility."
                ]
            }

        # ---- Build structured event
        event = {
            "event": event_data["name"],
            "visibility": visibility,
            "features": features,
            "explanation": ai_explanation
        }

        # =========================
        # STORE ONLY USEFUL EVENTS (Recommended)
        # =========================
        if visibility != "LOW":
            TODAY_EVENTS.append(event)

    print("TODAY IMPORTANT EVENTS BUILT:")
    print(TODAY_EVENTS)




def start_scheduler():

    scheduler = BackgroundScheduler()

    # =========================
    # RUN ON SERVER START
    # =========================
    print("Running initial daily celestial scan...")
    scan_events()

    # =========================
    # DAILY UPDATE AT MIDNIGHT
    # =========================
    # hour=0, minute=0 means 12:00 AM
    scheduler.add_job(
        scan_events,
        trigger='cron',
        hour=0,
        minute=0
    )

    scheduler.start()
