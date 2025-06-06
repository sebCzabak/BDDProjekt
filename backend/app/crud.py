from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date



def get_rates_by_date(db: Session, effective_date: date) -> list[models.CurrencyRate]:
    print(f"\n[CRUD.GET] Rozpoczynam wyszukiwanie w bazie dla daty: {effective_date}")
    result = db.query(models.CurrencyRate).filter(models.CurrencyRate.effective_date == effective_date).all()
    print(f"[CRUD.GET] Zapytanie zakończone. Znaleziono {len(result)} rekordów.")
    return result

def get_rate_by_code_and_date(db: Session, code: str, effective_date: date):

    return db.query(models.CurrencyRate).filter(
        models.CurrencyRate.currency_code == code,
        models.CurrencyRate.effective_date == effective_date
    ).first()



def save_rates(db: Session, rates: list[dict]):
    print("\n[CRUD.SAVE] Rozpoczynam funkcję save_rates.")
    print(f"[CRUD.SAVE] Otrzymano {len(rates)} stawek do przetworzenia.")
    new_rates_count = 0
    
    for rate_data in rates:
        effective_date_obj = date.fromisoformat(rate_data["effective_date"])
        db_rate = get_rate_by_code_and_date(db, code=rate_data["currency_code"], effective_date=effective_date_obj)
        
        if not db_rate:
            new_rate = models.CurrencyRate(
                currency_name=rate_data["currency_name"],
                currency_code=rate_data["currency_code"],
                rate=rate_data["rate"],
                effective_date=effective_date_obj
            )
            db.add(new_rate)
            new_rates_count += 1

    print(f"[CRUD.SAVE] Pętla zakończona. Dodano do sesji {new_rates_count} nowych stawek.")
    
    if new_rates_count > 0:
        try:
            print("[CRUD.SAVE] Próbuję wykonać db.commit()...")
            db.commit()
            print("[CRUD.SAVE] SUKCES! db.commit() wykonany pomyślnie.")
        except Exception as e:
            print(f"[CRUD.SAVE] BŁĄD KRYTYCZNY PODCZAS db.commit(): {e}")
            db.rollback()
    else:
        print("[CRUD.SAVE] Nie było nic do zapisania, pomijam db.commit().")
        
    return new_rates_count



def get_rates_by_date_range(db: Session, start_date: date, end_date: date) -> list[models.CurrencyRate]:
    return db.query(models.CurrencyRate).filter(
        models.CurrencyRate.effective_date >= start_date,
        models.CurrencyRate.effective_date <= end_date
    ).order_by(models.CurrencyRate.effective_date, models.CurrencyRate.currency_code).all()

def get_distinct_currencies(db: Session) -> list[tuple[str, str]]:
    return db.query(
        models.CurrencyRate.currency_code,
        models.CurrencyRate.currency_name
    ).distinct().order_by(models.CurrencyRate.currency_code).all()