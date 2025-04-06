from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# Load the trained model and encoders
model = joblib.load("sneaker_model.pkl")
brand_encoder = joblib.load("brand_encoder.pkl")
model_encoder = joblib.load("model_encoder.pkl")
edition_encoder = joblib.load("edition_encoder.pkl")

# Input schema
class SneakerInput(BaseModel):
    retail_price: float
    sale_price: float
    release_year: int
    brand: str
    model: str
    edition: str

# Create FastAPI app
app = FastAPI()

@app.post("/predict")
def predict(data: SneakerInput):
    # Encode categorical inputs
    brand_encoded = brand_encoder.transform([data.brand])[0]
    model_encoded_val = model_encoder.transform([data.model])[0]
    edition_encoded = edition_encoder.transform([data.edition])[0]

    # Prepare the features
    features = np.array([[data.retail_price, data.sale_price, data.release_year,
                          brand_encoded, model_encoded_val, edition_encoded]])

    prediction = model.predict(features)
    return {"hyped": int(prediction[0])}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:5500"] or your frontend port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
