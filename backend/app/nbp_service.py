import httpx
from datetime import date
import logging

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NBP_API_URL = "http://api.nbp.pl/api/exchangerates/tables/A"

async def fetch_rates_for_date(fetch_date: date) -> list[dict] | None:
    """
    Pobiera kursy walut z API NBP dla podanej daty.
    """
    url = f"{NBP_API_URL}/{fetch_date.strftime('%Y-%m-%d')}/"
    logger.info(f"Wysyłanie zapytania do NBP API: {url}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params={"format": "json"})
            response.raise_for_status()  # Rzuci wyjątkiem dla kodów 4xx/5xx
            
            data = response.json()
            if not data or not isinstance(data, list) or not data[0].get("rates"):
                logger.warning("Otrzymano nieprawidłowe dane z NBP API.")
                return None

            # Przetwarzamy dane do prostszej struktury
            effective_date = data[0].get("effectiveDate")
            rates = [
                {
                    "currency_name": rate.get("currency"),
                    "currency_code": rate.get("code"),
                    "rate": rate.get("mid"),
                    "effective_date": effective_date,
                }
                for rate in data[0]["rates"]
            ]
            logger.info(f"Pomyślnie pobrano {len(rates)} kursów dla daty {effective_date}.")
            return rates

        except httpx.HTTPStatusError as e:
            # NBP zwraca 404, gdy dla danego dnia nie ma notowań (np. weekend, święto)
            if e.response.status_code == 404:
                logger.warning(f"Brak danych o kursach dla daty {fetch_date} (status 404).")
            else:
                logger.error(f"Błąd HTTP podczas zapytania do NBP API: {e}")
            return None
        except Exception as e:
            logger.error(f"Niespodziewany błąd: {e}")
            return None