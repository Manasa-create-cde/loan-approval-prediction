from typing import Literal
from pydantic import BaseModel, Field


class LoanInput(BaseModel):
    # Same names as the training data columns
    no_of_dependents: int = Field(..., ge=0, le=5)
    education: Literal["Graduate", "Not Graduate"]
    self_employed: Literal["Yes", "No"]
    income_annum: int = Field(..., gt=0)
    loan_amount: int = Field(..., gt=0)
    loan_term: int = Field(..., ge=2, le=20)  # in years
    cibil_score: int = Field(..., ge=300, le=900)
    residential_assets_value: int = Field(..., ge=-100000)
    commercial_assets_value: int = Field(..., ge=0)
    luxury_assets_value: int = Field(..., ge=0)
    bank_asset_value: int = Field(..., ge=0)


class PredictionOut(BaseModel):
    # What FastAPI will send back to React
    prediction: str