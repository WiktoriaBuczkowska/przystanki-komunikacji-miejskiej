# API
**Antoni Mikołajdu-Skrzypczak** (Osoba 3)

- REST API w Pythonie (FastAPI) odczytujące dane z bazy przystanków
- endpointy: lista przystanków w GeoJSON (`/stops`), statystyki (`/stats`), najbliższy przystanek (`/stops/nearest`)
- wyszukiwanie najbliższego przystanku na podstawie odległości geograficznej (wzór haversine'a)
- testy jednostkowe w pytest (`tests/`) i dokumentacja uruchomienia API
