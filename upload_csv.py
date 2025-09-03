# upload_csv.py
import csv
import json
import sys
import os

def read_csv():
    events = []
    try:
        with open('events.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # String → float dönüşümü
                lat = float(row["latitude"]) if row["latitude"] else None
                lng = float(row["longitude"]) if row["longitude"] else None
                events.append({
                    "ad": row["ad"],
                    "tarih": row["tarih"],
                    "saat": row["saat"],
                    "mekan_adi": row["mekan_adi"],
                    "link": row["link"],
                    "aciklama": row["aciklama"],
                    "latitude": lat,
                    "longitude": lng
                })
        print(f"{len(events)} etkinlik CSV'den yüklendi.", file=sys.stderr)
    except Exception as e:
        print(f"❌ CSV okuma hatası: {e}", file=sys.stderr)
    return events

if __name__ == "__main__":
    events = read_csv()
    json.dump(events, sys.stdout)
    sys.stdout.flush()