from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import torch
import torch.nn as nn
import numpy as np
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Inference Service", version="1.0.0")

REQUEST_COUNT = Counter('inference_requests_total', 'Total inference requests')
REQUEST_LATENCY = Histogram('inference_request_duration_seconds', 'Inference request latency')
ERROR_COUNT = Counter('inference_errors_total', 'Total inference errors')

class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.fc2 = nn.Linear(50, 20)
        self.fc3 = nn.Linear(20, 1)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = SimpleModel()
model.eval()

class InferenceRequest(BaseModel):
    data: list[float]

class InferenceResponse(BaseModel):
    prediction: float
    latency_ms: float

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ai-inference"}

@app.get("/ready")
def readiness_check():
    return {"status": "ready", "model_loaded": True}

@app.post("/predict", response_model=InferenceResponse)
def predict(request: InferenceRequest):
    start_time = time.time()
    REQUEST_COUNT.inc()
    
    try:
        if len(request.data) != 10:
            ERROR_COUNT.inc()
            raise HTTPException(status_code=400, detail="Input must have 10 features")
        
        input_tensor = torch.tensor([request.data], dtype=torch.float32)
        
        with torch.no_grad():
            prediction = model(input_tensor)
        
        latency = (time.time() - start_time) * 1000
        REQUEST_LATENCY.observe(time.time() - start_time)
        
        return InferenceResponse(
            prediction=float(prediction.item()),
            latency_ms=round(latency, 2)
        )
    except Exception as e:
        ERROR_COUNT.inc()
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
