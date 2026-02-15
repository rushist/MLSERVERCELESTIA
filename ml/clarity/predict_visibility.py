import joblib
import numpy as np

# Load model only once (important for performance)
model = joblib.load("models/visibility_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

def predict_visibility(features_dict):

    features = np.array([[
        features_dict["cloud_cover"],
        features_dict["altitude"],
        features_dict["duration"],
        features_dict["moon_phase"],
        features_dict["light_pollution"],
        features_dict["hour"]
    ]])

    pred = model.predict(features)[0]

    label = label_encoder.inverse_transform([pred])[0]

    return label
