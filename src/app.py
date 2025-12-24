import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import os 

# with open("models/final_model.pkl", "rb") as f:
#     model = pickle.load(f)

# mlflow.set_tracking_uri(
#     os.getenv("MLFLOW_TRACKING_URI", "http://192.168.1.1:5001")
# )
# MODEL_NAME = "HeartDiseaseClassifier"
# MODEL_VERSION = "1"

# # Load model at startup
# model = mlflow.sklearn.load_model(
#     model_uri=f"models:/{MODEL_NAME}/{MODEL_VERSION}"
# )

# No tracking URI needed if loading from local path!
import mlflow.sklearn

import mlflow
from mlflow import artifacts

# # Define the model URI
# model_uri = "models:/HeartDiseaseClassifier/staging"
# # Define the local directory to download the model
# local_dir = "./exported_model"
# # Download the model artifacts
# local_path = mlflow.artifacts.download_artifacts(artifact_uri=model_uri, dst_path=local_dir)
# print("======================")
# print(local_path)
model = mlflow.sklearn.load_model(model_uri="exported_model")

app = FastAPI(title="Heart Disease Prediction API")

class PatientInput(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

@app.post("/predict")
def predict(data: PatientInput):
    df = pd.DataFrame([data.dict()])
    prediction = int(model.predict(df)[0])

    try:
        proba = model.predict_proba(df)[0]
        confidence = float(proba[prediction])
    except Exception as e:
        print(f"DEBUG: Probability failed with error: {e}") # This will show in your Docker logs
        confidence = None

    return {"prediction": prediction, "confidence": confidence}