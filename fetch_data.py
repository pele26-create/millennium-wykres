import urllib.request
import json
import csv

STOOQ_URL = "https://stooq.pl/q/d/l/?s=4095.pl&i=d"

def fetch_and_convert():
    req = urllib.request.Request(STOOQ_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            csv_data = response.read().decode('utf-8').strip().splitlines()
            
            reader = csv.reader(csv_data)
            header = next(reader, None)
            
            parsed_data = []
            for row in reader:
                if len(row) >= 5:
                    date_str = row[0].strip()
                    try:
                        nav_val = float(row[4].strip())
                        parsed_data.append({"date": date_str, "nav": nav_val})
                    except ValueError:
                        continue
            
            parsed_data.sort(key=lambda x: x["date"])
            
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(parsed_data, f, indent=2)
                
            print(f"Pomyślnie zapisano {len(parsed_data)} rekordów do data.json")
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")

if __name__ == "__main__":
    fetch_and_convert()
