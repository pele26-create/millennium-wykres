import urllib.request
import json
import os

URL = "https://stooq.pl/q/d/l/?s=1081.pl&i=d"

def fetch_latest_data():
    data = []
    
    try:
        # Dodajemy nagłówek udający standardową przeglądarkę, by uniknąć blokady bota
        req = urllib.request.Request(
            URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            csv_text = response.read().decode('utf-8')
        
        lines = csv_text.strip().split('\n')
        
        # Omijamy pierwszy wiersz (nagłówki: Data, Otwarcie, Najwyzszy...)
        for line in lines[1:]:
            parts = line.split(',')
            # Upewniamy się, że linijka ma przynajmniej 5 elementów i pierwszy wygląda jak data (np. 2024-01-02)
            if len(parts) >= 5 and '-' in parts[0]:
                date_str = parts[0].strip()
                try:
                    # Cena zamknięcia to 5 element w CSV na Stooq (indeks 4)
                    close_price = float(parts[4].strip())
                    if close_price > 50: # Bezpiecznik: zakładamy, że wycena funduszu nie spadnie nagle poniżej 50 PLN
                        data.append({"date": date_str, "nav": close_price})
                except ValueError:
                    continue

        print(f"Pobrano {len(data)} prawidłowych rekordów dziennych ze Stooq.")

    except Exception as e:
        print(f"Błąd podczas pobierania lub parsowania danych ze Stooq: {e}")

    # Jeśli nie udało się pobrać żadnych poprawnych danych, NIE nadpisujemy pliku pustą tablicą
    if len(data) < 100:
        print("Pobrano zbyt mało danych lub wystąpił błąd. Skrypt nie nadpisze pliku data.json.")
        # Zakończ działanie skryptu z błędem, aby GitHub Actions pokazało czerwony krzyżyk,
        # ale stary, dobry data.json (jeśli istnieje) pozostał nietknięty.
        exit(1)
        
    else:
        # Jeśli wszystko poszło dobrze, zapisujemy dane
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, separators=(',', ':')) # Używamy minifikacji, aby plik ładował się szybciej
        print("Zaktualizowano plik data.json nowymi danymi dziennymi.")

if __name__ == "__main__":
    fetch_latest_data()
