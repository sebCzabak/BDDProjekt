# backend/tests/test_api.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import date

from app.models import CurrencyRate

def test_read_rates_by_date_success(test_client: TestClient, db_session: Session):
    """
    Scenario: Pomyślne pobranie kursów dla dnia, w którym dane istnieją
    """
    # Given: W bazie danych znajduje się kurs dla waluty 'TSC' z dnia 2025-06-09
    test_date = date(2025, 6, 9)
    rate_to_add = CurrencyRate(
        currency_name="Testcoin", 
        currency_code="TSC", 
        rate=5.0, 
        effective_date=test_date
    )
    db_session.add(rate_to_add)

    # When: Wysyłam zapytanie GET na endpoint "/currencies/2025-06-09"
    response = test_client.get(f"/currencies/{test_date.strftime('%Y-%m-%d')}")

    # Then: Otrzymuję odpowiedź ze statusem 200 OK
    assert response.status_code == 200

    # And: Odpowiedź zawiera listę z jednym kursem waluty
    data = response.json()
    assert len(data) == 1

    # And: Kurs na liście ma kod "TSC"
    assert data[0]["currency_code"] == "TSC"


def test_read_rates_by_date_not_found(test_client: TestClient):
    """
    Scenario: Próba pobrania kursów dla dnia, w którym dane nie istnieją
    """
    # Given: Baza danych jest pusta dla szukanej daty

    # When: Wysyłam zapytanie GET na endpoint "/currencies/2025-01-01"
    response = test_client.get("/currencies/2025-01-01")

    # Then: Otrzymuję odpowiedź ze statusem 404 Not Found
    assert response.status_code == 404