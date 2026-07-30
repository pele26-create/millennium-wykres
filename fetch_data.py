import urllib.request
import re
import json
import os

# Ticker funduszu Millennium Multistrategia SFIO kat. A na Stooq
URL = "https://stooq.pl/q/d/l/?s=1081.pl&i=d"

def fetch_latest_data():
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            csv_text = response.read().decode('utf-8')
        
        lines = csv_text.strip().split('\n')
        data = []
        
        # Omijamy nagłówek CSV (Data, Otwarcie, Najwyzszy, Najnizszy, Zamkniecie)
        for line in lines[1:]:
            parts = line.split(',')
            if len(parts) >= 5:
                date_str = parts[0]
                try:
                    close_price = float(parts[4])
                    data.append({"date": date_str, "nav": close_price})
                except ValueError:
                    continue

        # Zapisujemy wyciągnięte dane do pliku data.json
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"Pomyślnie pobrano {len(data)} wpisów.")

    except Exception as e:
        print("Błąd podczas pobierania danych:", e)

if __name__ == "__main__":
    fetch_latest_data()
