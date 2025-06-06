# Aplikacja do Kursów Walut NBP

## Opis Projektu

Jest to w pełni funkcjonalna, skonteneryzowana aplikacja internetowa typu Full-Stack, która umożliwia pobieranie, wyświetlanie i analizę historycznych kursów walut z publicznego API Narodowego Banku Polskiego. Projekt został zrealizowany z naciskiem na nowoczesne praktyki deweloperskie, w tym konteneryzację (Docker), architekturę z podziałem na niezależne moduły oraz implementację testów automatycznych w podejściu BDD.

---

## Główne Funkcjonalności

* **Pobieranie danych na żądanie:** Możliwość zasilenia bazy danych kursami walut dla wybranego dnia za pomocą endpointu API.
* **Dynamiczne przeglądanie danych:** Interfejs użytkownika pozwala na interaktywne wyświetlanie kursów walut z podziałem na:
    * Dni
    * Miesiące
    * Kwartały
    * Lata
* **Architektura wielomodułowa:** Jasny podział na niezależne serwisy:
    * **Frontend:** Aplikacja kliencka w Angularze.
    * **Backend:** API REST w FastAPI (Python).
    * **Baza Danych:** Serwer PostgreSQL.
* **Testy automatyczne:** Projekt zawiera zestaw testów jednostkowych i integracyjnych dla backendu (`pytest`) oraz testów jednostkowych dla frontendu (`Karma`/`Jasmine`), napisanych z uwzględnieniem zasad BDD.

---

## Stos Technologiczny

**Backend:**
* **Framework:** FastAPI (Python)
* **Baza Danych:** PostgreSQL
* **Komunikacja z bazą:** SQLAlchemy (ORM)
* **Migracje bazy danych:** Alembic
* **Testowanie:** PyTest

**Frontend:**
* **Framework:** Angular
* **Stylizacja:** SCSS
* **Testowanie:** Karma, Jasmine

**Infrastruktura i Narzędzia:**
* **Konteneryzacja:** Docker, Docker Compose
* **Serwer WWW dla frontendu:** Nginx (działający jako reverse proxy)
* **Zewnętrzne API:** Narodowy Bank Polski (api.nbp.pl)

---

## Uruchomienie Aplikacji

Dzięki konteneryzacji, uruchomienie całego środowiska jest niezwykle proste.

### Wymagania wstępne

* Zainstalowany [Docker](https://www.docker.com/products/docker-desktop/) i Docker Compose.

### Instrukcja uruchomienia

1.  Sklonuj repozytorium na swój lokalny dysk.
2.  Otwórz terminal w głównym katalogu projektu.
3.  Wykonaj jedno polecenie, które zbuduje obrazy i uruchomi wszystkie kontenery:
    ```bash
    docker-compose up --build
    ```
4.  Poczekaj, aż wszystkie serwisy wystartują. Proces może potrwać kilka minut przy pierwszym uruchomieniu.
5.  Otwórz przeglądarkę i wejdź na adres:
    `http://localhost:4200`

### Zasilanie bazy danych

Aplikacja startuje z pustą bazą danych. Aby załadować dane:
1.  Przejdź do dokumentacji API backendu: `http://localhost:8000/docs`.
2.  Użyj endpointu `POST /currencies/fetch`, aby pobrać kursy dla wybranego dnia. Możesz wykonać to zapytanie wielokrotnie dla różnych dat, aby zapełnić bazę.

---

## Uruchamianie Testów

Testy są uruchamiane wewnątrz odpowiednich kontenerów Docker.

### Testy Backendu

Aby uruchomić zestaw testów `pytest` dla backendu, wykonaj polecenie:

```bash
docker-compose exec backend pytest
```

### Testy Frontendu

Aby uruchomić testy `Karma/Jasmine` dla frontendu, wykonaj polecenie w **osobnym terminalu**:

```bash
# Przejdź do katalogu frontendu
cd frontend

# Uruchom testy
ng test
```