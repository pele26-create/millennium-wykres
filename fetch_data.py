import urllib.request
import json
import re

# Alternatywne źródło API wycen dla Millennium Multistrategia kat. A
URL = "https://stooq.pl/q/d/l/?s=1081.pl&i=d"

def update_daily_data():
    existing_data = []
    
    # 1. Odczytujemy istniejący plik data.json
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except Exception as e:
        print("Nie udało się odczytać obecnego data.json:", e)

    # 2. Pobieramy nową wycenę ze stooq z nowym Headerem
    try:
        req = urllib.request.Request(
            URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            csv_text = response.read().decode('utf-8')
        
        lines = csv_text.strip().split('\n')
        fetched_dict = {}
        
        for line in lines[1:]:
            parts = line.split(',')
            if len(parts) >= 5 and '-' in parts[0]:
                date_str = parts[0].strip()
                try:
                    close_price = float(parts[4].strip())
                    if close_price > 50:
                        fetched_dict[date_str] = close_price
                except ValueError:
                    continue

        if len(fetched_dict) > 0:
            # Łączymy dane i sortujemy po dacie
            merged = {item['date']: item['nav'] for item in existing_data}
            merged.update(fetched_dict)
            
            sorted_data = [{"date": k, "nav": merged[k]} for k in sorted(merged.keys())]
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(sorted_data, f, indent=2)
            print(f"Sukces! Baza zawiera teraz {len(sorted_data)} rekordów dziennych.")
            return

    except Exception as e:
        print("Problem z pobraniem sieciowym:", e)

    print("Zachowano obecny plik data.json bez zmian.")

if __name__ == "__main__":
    update_daily_data()
