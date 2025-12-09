from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from schemas import ComplaintRequest, PredictionResponse
from model_service import ModelService

model_service = ModelService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Uygulama başlarken modeli yükle
    model_service.load_model()
    yield
    # Uygulama kapanırken yapılacaklar (varsa)

app = FastAPI(title="AI Complaint Classification Service", lifespan=lifespan)

@app.post("/predict", response_model=PredictionResponse)
async def predict_complaint(request: ComplaintRequest):
    try:
        prediction = model_service.predict(request.text)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "active", "model_loaded": model_service.model is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)