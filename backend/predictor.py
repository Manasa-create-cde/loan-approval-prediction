from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from schemas import LoanInput

# Path to the saved model, relative to this file
MODEL_PATH = Path(__file__).parent / "model" / "loan_model.pkl"

# Load the model ONCE when the app starts (not on every request)
model = joblib.load(MODEL_PATH)

# Same encodings as the training notebook (LabelEncoder sorts alphabetically)
EDUCATION_MAP = {"Graduate": 0, "Not Graduate": 1}
SELF_EMPLOYED_MAP = {"No": 0, "Yes": 1}

# Model output: 0 = Approved, 1 = Rejected
RESULT_MAP = {0: "Loan Approved", 1: "Loan Not Approved"}


def preprocess(data: LoanInput) -> pd.DataFrame:
    """Turn the 11 raw inputs into the model's 12 features (same as training)."""
    row = {
        "no_of_dependents": data.no_of_dependents,
        "education": EDUCATION_MAP[data.education],
        "self_employed": SELF_EMPLOYED_MAP[data.self_employed],
        "cibil_score": data.cibil_score,
        "residential_assets_value": data.residential_assets_value,
        "commercial_assets_value": data.commercial_assets_value,
        "luxury_assets_value": data.luxury_assets_value,
        "bank_asset_value": data.bank_asset_value,
        "Total_Applicant": data.income_annum,
        "ApplicantIncomelog": np.log(data.income_annum + 1),
        "loan_amount_log": np.log(data.loan_amount + 1),
        "loan_term_log": np.log(data.loan_term + 1),
    }
    # Use the exact feature order the model was trained with
    return pd.DataFrame([row])[list(model.feature_names_in_)]


def predict_loan(data: LoanInput) -> str:
    features = preprocess(data)
    result = int(model.predict(features)[0])
    return RESULT_MAP[result]