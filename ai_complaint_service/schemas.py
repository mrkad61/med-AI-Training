from pydantic import BaseModel
from typing import List

class ComplaintRequest(BaseModel):
    text: str

class Prediction(BaseModel):
    label: str
    score: float

class PredictionResponse(BaseModel):
    label: str
    score: float
    predictions: List[Prediction]
