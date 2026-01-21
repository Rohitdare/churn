from fastapi import FastAPI
from pydantic import BaseModel
from .predict import predict_churn

app = FastAPI(title="SaaS Churn Prediction API")


class AccountFeatures(BaseModel):
    seats: int
    is_trial: int
    account_age_days: int

    industry_DevTools: bool
    industry_EdTech: bool
    industry_FinTech: bool
    industry_HealthTech: bool

    country_CA: bool
    country_DE: bool
    country_FR: bool
    country_IN: bool
    country_UK: bool
    country_US: bool

    referral_source_event: bool
    referral_source_organic: bool
    referral_source_other: bool
    referral_source_partner: bool

    plan_tier_Enterprise: bool
    plan_tier_Pro: bool 


@app.post("/predict")
def predict(account: AccountFeatures):
    return predict_churn(account.dict())
