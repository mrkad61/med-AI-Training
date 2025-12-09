from pydantic import BaseModel

class ComplaintRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    label: str
    score: float
