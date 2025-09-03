# scrape_google_events.py
import requests
import json
import sys

def scrape_google_events():
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_events",
        "q": "etkinlikler Türkiye",
        "hl": "tr",
        "api_key": "YOUR_API_KEY"
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        if response.status_code == 429:
            print("❌ SerpApi: Ücretsiz kota doldu (429)", file=sys.stderr)
            return []

        response.raise_for_status()
        data = response.json()

        events = []
        for event in data.get("events", []):
            try:
                # Tarih
                date_info = event.get("date", {})
                start_date = date_info.get("start_date", "2025-01-01")

                # Saat (eğer varsa)
                when_text = date_info.get("when", "")
                time_str = "19:00"
                if when_text:
                    import re
                    time_match = re.search(r'(\d{1,2}:\d{2})', when_text)
                    if time_match:
                        time_str = time_match.group(1)

                # Mekan
                venue = event.get("location", {})
                venue_name = venue.get("name") or venue.get("address", "Bilinmeyen Mekan")

                # Koordinatlar
                gps = venue.get("gps_coordinates", {})
                lat = float(gps["latitude"]) if gps.get("latitude") else None
                lng = float(gps["longitude"]) if gps.get("longitude") else None

                events.append({
                    "ad": event["title"],
                    "tarih": start_date,
                    "saat": time_str,
                    "mekan_adi": venue_name,
                    "link": event.get("event_website") or event.get("google_event_link", "#"),
                    "aciklama": event.get("description", f"{venue_name} adresinde gerçekleşecek etkinlik."),
                    "latitude": lat,
                    "longitude": lng
                })
            except Exception as e:
                print(f"🟡 Etkinlik atlandı: {e}", file=sys.stderr)
                continue

        print(f"{len(events)} etkinlik Google'dan çekildi.", file=sys.stderr)
        return events

    except Exception as e:
        print(f"❌ Hata: {e}", file=sys.stderr)
        return []

# 🚀 Ana işlem
if __name__ == "__main__":
    events = scrape_google_events()
    json.dump(events, sys.stdout)
    sys.stdout.flush()