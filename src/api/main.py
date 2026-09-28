from pathlib import Path

import joblib

from fastapi import FastAPI

from .schemas import DeliveryPredictionRequest
from .utils import build_model_input

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "models"
    / "hist_gradient_optimized_pipeline.joblib"
)

print("Project root:", PROJECT_ROOT)
print("Model path:", MODEL_PATH)
print("Model exists:", MODEL_PATH.exists())
model = joblib.load(MODEL_PATH)


app = FastAPI(
    title="Delivery Time Prediction API",
    description="Predict delivery time using the trained delivery model",
)


@app.get("/")
def root():

    return {
        "message": "Delivery prediction API is working",
    }


@app.post("/predict")
def predict(
    data: DeliveryPredictionRequest,
):
    features = build_model_input(data)
    if hasattr(model, "feature_names_in_"):
        features = features[list(model.feature_names_in_)]
    prediction = model.predict(features)[0]
    return {"predicted_delivery_time_minutes": round(float(prediction), 2)}
