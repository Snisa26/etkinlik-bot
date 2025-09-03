# scrape_passo.py
import requests
import sys
import json

def scrape_passo():
    url = "https://cppasso2.mediatriple.net/30s/api/passoweb/getalleventgroups"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://passo.com.tr",
        "Origin": "https://passo.com.tr"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"API hatası: {e}", file=sys.stderr)
        return []

    events = []
    
    # API yanıtını incele: data içinde mi? result içinde mi?
    event_list = data.get("data", [])  # Veya data.get("result", []) vs.

    for item in event_list:
        try:
            # Gerekli alanlar var mı kontrol et
            if not item.get("name") or not item.get("eventDate") or not item.get("venue"):
                continue

            # Tarih formatı: "2025-09-04T20:00:00" → "2025-09-04"
            raw_date = item["eventDate"]
            date_part = raw_date.split("T")[0]  # "2025-09-04"
            time_part = raw_date.split("T")[1][:5] if "T" in raw_date else "19:00"  # "20:00"

            venue = item["venue"]
            lat = float(venue["latitude"]) if venue.get("latitude") else None
            lng = float(venue["longitude"]) if venue.get("longitude") else None

            events.append({
                "ad": item["name"],
                "tarih": date_part,
                "saat": time_part,
                "mekan_adi": venue["name"],
                "link": f"https://passo.com.tr/etkinlik/{item['id']}",
                "aciklama": item.get("shortDescription", "Detay bulunamadı"),
                "latitude": lat,
                "longitude": lng
            })
        except Exception as e:
            print(f"Veri işleme hatası: {e}", file=sys.stderr)
            continue

    print(f"{len(events)} etkinlik çekildi.", file=sys.stderr)
    return events

# 🚀 Ana işlem
if __name__ == "__main__":
    events = scrape_passo()
    json.dump(events, sys.stdout)
    sys.stdout.flush()
