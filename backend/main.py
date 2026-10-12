from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from predictor import predict_loan
from schemas import LoanInput, PredictionOut

# Create the table in MySQL if it doesn't exist yet
Base.metadata.create_all(bind=engine)

# Create the FastAPI application
app = FastAPI(title="Loan Prediction API")

# CORS: allow the React app (Vite runs on port 5173) to call this backend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Test route: just to check that the server is running
@app.get("/")
def home():
    return {"message": "Loan Prediction API is running"}


@app.post("/predict", response_model=PredictionOut)
def predict(data: LoanInput, db: Session = Depends(get_db)):
    # 1. Preprocess + run the ML model
    try:
        result = predict_loan(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # 2. Save the application and result to MySQL
    try:
        application = models.LoanApplication(**data.model_dump(), prediction=result)
        db.add(application)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not save to database: {str(e)}")

    # 3. Return the prediction
    return {"prediction": result}