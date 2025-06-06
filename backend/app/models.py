from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    id = Column(Integer, primary_key=True, index=True)
    currency_name = Column(String, index=True)
    currency_code = Column(String, index=True)
    rate = Column(Float)
    effective_date = Column(Date, index=True)