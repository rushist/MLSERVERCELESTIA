import random
import pandas as pd

rows = []

for _ in range(1200):   # generate 1200 samples

    cloud_cover = random.randint(0,100)
    altitude = random.randint(5,90)
    duration = random.randint(1,10)
    moon_phase = random.randint(0,100)
    light_pollution = random.randint(1,10)
    hour = random.randint(0,23)

    score = 0

    if altitude > 50:
        score += 2
    if duration > 5:
        score += 1
    if cloud_cover < 30:
        score += 2
    if moon_phase < 50:
        score += 1
    if light_pollution < 5:
        score += 2
    if hour >= 18 or hour <= 6:
        score += 2

    if score >= 7:
        visibility = "HIGH"
    elif score >= 4:
        visibility = "MEDIUM"
    else:
        visibility = "LOW"

    rows.append([
        cloud_cover,
        altitude,
        duration,
        moon_phase,
        light_pollution,
        hour,
        visibility
    ])

df = pd.DataFrame(rows, columns=[
    "cloud_cover",
    "altitude",
    "duration",
    "moon_phase",
    "light_pollution",
    "hour",
    "visibility"
])

df.to_csv("visibility_dataset.csv", index=False)

print("Dataset Generated Successfully")
