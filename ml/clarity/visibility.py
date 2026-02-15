import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# =====================
# 1. LOAD DATASET
# =====================
data = pd.read_csv("data/visibility_dataset.csv")

# =====================
# 2. SEPARATE FEATURES
# =====================
X = data.drop("visibility", axis=1)
y = data["visibility"]

# Encode labels: HIGH/MEDIUM/LOW → numbers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# =====================
# 3. TRAIN TEST SPLIT
# =====================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

# =====================
# 4. TRAIN MODEL
# =====================
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=8,
    random_state=42
)

model.fit(X_train, y_train)

# =====================
# 5. EVALUATE MODEL
# =====================
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nReport:\n", classification_report(y_test, y_pred))

# =====================
# 6. SAVE MODEL
# =====================
joblib.dump(model, "models/visibility_model.pkl")
joblib.dump(label_encoder, "models/label_encoder.pkl")

print("\nModel saved successfully!")
