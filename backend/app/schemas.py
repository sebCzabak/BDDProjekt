from pydantic import BaseModel, ConfigDict # 
from datetime import date

class CurrencyRateBase(BaseModel):
    currency_name: str
    currency_code: str
    rate: float
    effective_date: date

class CurrencyRateCreate(CurrencyRateBase):
    pass

class CurrencyRate(CurrencyRateBase):
    id: int


    model_config = ConfigDict(from_attributes=True)