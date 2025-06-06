from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas, crud, nbp_service
from .database import SessionLocal 


#models.Base.metadata.create_all(bind=engine) 

app = FastAPI(title="Currency Exchange API")

origins = ["http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Witaj w API do kursów walut!"}

@app.post("/currencies/fetch", tags=["Currencies"], status_code=201)
async def fetch_and_save_rates(fetch_date: date, db: Session = Depends(get_db)):
    print(f"\n[MAIN.POST] Otrzymano żądanie POST /fetch dla daty: {fetch_date}")
    rates_data = await nbp_service.fetch_rates_for_date(fetch_date)

    if not rates_data:
        print(f"[MAIN.POST] Błąd: NBP Service nie zwrócił danych dla {fetch_date}.")
        raise HTTPException(status_code=404, detail=f"Nie znaleziono kursów walut dla daty {fetch_date}.")

    print(f"[MAIN.POST] Pobrane dane z NBP. Przekazuję do crud.save_rates...")
    newly_added_count = crud.save_rates(db=db, rates=rates_data)
    print(f"[MAIN.POST] crud.save_rates zakończone. Zapisano {newly_added_count} nowych stawek.")
    
    return {
        "message": "Pobieranie i zapisywanie zakończone.",
        "fetch_date": fetch_date,
        "newly_added_rates": newly_added_count,
        "total_rates_processed": len(rates_data)
    }

@app.get("/currencies/{effective_date}", response_model=List[schemas.CurrencyRate], tags=["Currencies"])
def read_rates_by_date(effective_date: date, db: Session = Depends(get_db)):
    print(f"\n[MAIN.GET] Otrzymano żądanie GET /currencies/{effective_date}")
    rates = crud.get_rates_by_date(db, effective_date=effective_date)
    print(f"[MAIN.GET] crud.get_rates_by_date zwróciło {len(rates)} rekordów.")

    if not rates:
        print(f"[MAIN.GET] Nie znaleziono stawek, zwracam 404.")
        raise HTTPException(status_code=404, detail=f"Nie znaleziono kursów dla daty {effective_date} w bazie danych.")
    
    print(f"[MAIN.GET] Znaleziono stawki, zwracam 200 OK.")
    return rates


@app.get("/currencies", response_model=List[schemas.CurrencyRate], tags=["Currencies"])
def read_rates_by_date_range(start_date: date, end_date: date, db: Session = Depends(get_db)):
    rates = crud.get_rates_by_date_range(db, start_date=start_date, end_date=end_date)
    return rates

@app.get("/currencies/meta/distinct", tags=["Currencies Meta"])
def read_distinct_currencies(db: Session = Depends(get_db)):
    currencies = crud.get_distinct_currencies(db)
    return [{"code": code, "name": name} for code, name in currencies]