# Testy manualne API

Data: 24.11.2026
Sposób: uruchomienie API i wywołanie endpointów (Swagger UI, /docs)

| Endpoint | Oczekiwany wynik | Wynik | Status |
|---|---|---|---|
| `GET /` | status „ok” | `{"status": "ok"}` | ✅ |
| `GET /stops` | lista przystanków w GeoJSON | FeatureCollection, 1864 przystanki | ✅ |
| `GET /stats` | statystyki przystanków | 1864 przystanki: 1392 autobusowe, 321 tramwajowe, 150 wspólnych, 1 inny; 1113 z wiatą | ✅ |
| `GET /stops/nearest?lat=51.1098&lon=17.0315` (Rynek) | najbliższy przystanek | „Oławska” (tramwaj), 216.9 m | ✅ |
| `GET /docs` | dokumentacja Swagger | strona się wyświetla | ✅ |

## Testy automatyczne
4 testy jednostkowe (pytest) uruchamiane automatycznie w GitHub Actions – wszystkie przechodzą.
