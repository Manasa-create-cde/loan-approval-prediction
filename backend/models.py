from sqlalchemy import Column, DateTime, Integer, String, func

from database import Base


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Inputs (same names as schemas.py)
    no_of_dependents = Column(Integer, nullable=False)
    education = Column(String(20), nullable=False)
    self_employed = Column(String(5), nullable=False)
    income_annum = Column(Integer, nullable=False)
    loan_amount = Column(Integer, nullable=False)
    loan_term = Column(Integer, nullable=False)
    cibil_score = Column(Integer, nullable=False)
    residential_assets_value = Column(Integer, nullable=False)
    commercial_assets_value = Column(Integer, nullable=False)
    luxury_assets_value = Column(Integer, nullable=False)
    bank_asset_value = Column(Integer, nullable=False)

    # Result and time
    prediction = Column(String(30), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)