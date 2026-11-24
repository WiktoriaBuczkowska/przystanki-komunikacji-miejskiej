# Przystanki komunikacji miejskiej – Wrocław

Projekt zespołowy realizowany w ramach zajęć. Celem jest stworzenie bazy danych przystanków komunikacji miejskiej we Wrocławiu, przedstawienie ich na mapie oraz udostępnienie danych za pomocą prostego API.

## Cel projektu
- zebranie danych o przystankach z otwartych źródeł
- utworzenie bazy danych z lokalizacjami przystanków
- wizualizacja przystanków na mapie w ArcGIS wraz z prostą analizą przestrzenną
- udostępnienie danych przez API w Pythonie

## Zespół

| Osoba | Rola |
|---|---|
| Julia Hinc | Dane i baza danych |
| Wojciech Karp | Wizualizacja i analizy w ArcGIS |
| Antoni Nikolajdu-Skrzypczak | API w Pythonie |
| Wiktoria Buczkowska | Docker, testy|

## Struktura repozytorium

| Folder | Zawartość |
| --- | --- |
| `data/` | dane i baza danych |
| `gis/` | projekt i mapy |
| `api/` | kod API |
| `tests/` | testy jednostkowe API |
| `docs/` | dokumentacja i harmonogram |

## Uruchomienie API (lokalnie)

1.  Zainstaluj wymagane biblioteki:

    ``` bash
    pip install -r requirements.txt
    ```

2.  Uruchom serwer FastAPI:

    ``` bash
    uvicorn api.main:app --reload
    ```

3.  Dokumentacja interaktywna (Swagger UI) jest dostępna pod adresem:
    `http://127.0.0.1:8000/docs`.

4.  Uruchom testy jednostkowe:

    ``` bash
    pytest
    ```

## Uruchomienie w Dockerze

Wymagany jest zainstalowany Docker. W głównym folderze projektu:

    docker compose up --build

API będzie dostępne pod adresem `http://localhost:8000`, a dokumentacja (Swagger UI) pod `http://localhost:8000/docs`.

## Testy automatyczne (CI)

Przy każdym wrzuceniu kodu do `main` i każdym Pull Requeście GitHub Actions automatycznie uruchamia testy jednostkowe oraz buduje i sprawdza kontener Dockera (zakładka **Actions**).


## Dostępne endpointy

-   `GET /` -- sprawdzenie statusu działania API
-   `GET /stops` -- lista wszystkich przystanków w formacie GeoJSON
    (`FeatureCollection`)
-   `GET /stats` -- podstawowe statystyki przystanków (liczba całkowita,
    podział na typ, obecność wiaty)
-   `GET /stops/nearest?lat=51.1098&lon=17.0315` -- wyszukiwanie
    najbliższego przystanku dla podanych współrzędnych
