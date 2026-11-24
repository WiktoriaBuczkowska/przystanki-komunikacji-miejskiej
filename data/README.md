# Dane i baza danych
**Julia Hinc** (Osoba 1)

- pobranie przystanków komunikacji miejskiej Wrocławia z OpenStreetMap (Overpass Turbo)
- utworzenie bazy SQLite/SpatiaLite `Przystanki.sqlite` (tabela `przystanki_sql`, 1864 przystanki)
- zapis geometrii punktów i atrybutów: nazwa, numer przystanku, rodzaj (autobus/tramwaj), wiata
