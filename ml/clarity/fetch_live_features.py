import requests
from datetime import datetime

def get_cloud_cover(lat, lon):

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=cloudcover"
    res = requests.get(url).json()

    # take current hour value
    cloud_cover = res["hourly"]["cloudcover"][0]

    return cloud_cover


def get_moon_phase():

    url = "https://api.freeastroapi.com/api/v1/moon/phase"
    res = requests.get(url).json()

    illumination = int(res["phase"]["illumination"] * 100)

    return illumination


def get_light_pollution(city):

    urban = ["mumbai","delhi","bangalore"]

    if city.lower() in urban:
        return 9
    return 5


def build_feature_object(lat, lon, city, altitude, duration):

    cloud_cover = get_cloud_cover(lat, lon)
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

    return features
