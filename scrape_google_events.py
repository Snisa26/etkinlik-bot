# scrape_google_events.py
import requests
import json
import sys
import os

def scrape_google_events():
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_events",
        "q": "etkinlikler Istanbul",   # Daha iyi sorgu
        "hl": "tr",
        "api_key": os.getenv("SERPAPI_KEY")
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        print(f"HTTP Status: {response.status_code}", file=sys.stderr)
        print(f"📜 API Yanıt: {response.text[:500]}", file=sys.stderr)  # 🔍 Logla

        if response.status_code == 429:
            print("❌ SerpApi: Kotan doldu (429)", file=sys.stderr)
            return []

        response.raise_for_status()
        data = response.json()

        if "error" in data:
            print(f"❌ API Hatası: {data['error']}", file=sys.stderr)
            return []

        events = []
        for event in data.get("events", []):
            try:
                date_info = event.get("date", {})
                start_date = date_info.get("start_date", "2025-01-01")

                when_text = date_info.get("when", "")
                time_str = "19:00"
                if when_text:
                    import re
                    time_match = re.search(r'(\d{1,2}:\d{2})', when_text)
                    if time_match:
                        time_str = time_match.group(1)

                venue = event.get("location", {})
                venue_name = venue.get("name") or venue.get("address", "Bilinmeyen Mekan")

                gps = venue.get("gps_coordinates", {})
                lat = float(gps["latitude"]) if gps.get("latitude") else None
                lng = float(gps["longitude"]) if gps.get("longitude") else None

                events.append({
                    "ad": event["title"],
                    "tarih": start_date,
                    "saat": time_str,
                    "mekan_adi": venue_name,
                    "link": event.get("event_website") or event.get("google_event_link", "#"),
                    "aciklama": event.get("description", f"{venue_name} adresinde etkinlik."),
                    "latitude": lat,
                    "longitude": lng
                })
            except Exception as e:
                print(f"🟡 Hata (etkinlik): {e}", file=sys.stderr)
                continue

        print(f"{len(events)} etkinlik Google'dan çekildi.", file=sys.stderr)
        return events

    except Exception as e:
        print(f"❌ Genel hata: {e}", file=sys.stderr)
        return []

# 🚀 Ana işlem
if __name__ == "__main__":
    events = scrape_google_events()
    json.dump(events, sys.stdout)
    sys.stdout.flush()
