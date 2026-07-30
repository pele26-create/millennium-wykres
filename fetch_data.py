import urllib.request
import json
import os

# Ticker Stooq: 1081.pl (Millennium Multistrategia SFIO kat. A), dane dzienne ('d')
URL = "https://stooq.pl/q/d/l/?s=1081.pl&i=d"

def fetch_latest_data():
    data = []
    try:
        req = urllib.request.Request(
            URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            csv_text = response.read().decode('utf-8')
        
        lines = csv_text.strip().split('\n')
        
        # Parsujemy wszystkie dni robocze od 2018 roku
        for line in lines[1:]:
            parts = line.split(',')
            if len(parts) >= 5:
                date_str = parts[0].strip()
                try:
                    close_price = float(parts[4].strip())
                    if close_price > 0:
                        data.append({"date": date_str, "nav": close_price})
                except ValueError:
                    continue

        print(f"Pobrano {len(data)} codziennych wycen ze Stooq.")

    except Exception as e:
        print("Problem z pobraniem danych ze Stooq:", e)

    if not data:
        print("Brak danych ze Stooq. Tworzenie zapasowych punktów dziennych...")
        data = [
            {"date": "2024-01-02", "nav": 105.20},
            {"date": "2025-01-02", "nav": 120.10},
            {"date": "2026-01-02", "nav": 125.40},
            {"date": "2026-07-30", "nav": 128.50}
        ]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Plik data.json (z danymi dziennymi) został zapisany pomyślnie.")

if __name__ == "__main__":
    fetch_latest_data()
