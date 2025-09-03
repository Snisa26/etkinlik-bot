# scrape_passo.py
import requests
import sys
import json
import time

def scrape_passo():
    base_url = "https://cppasso2.mediatriple.net/30s/api/passoweb"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://passo.com.tr/",
        "Origin": "https://passo.com.tr"
    }

    events = []

    # 1. Tüm grupları al
    try:
        response = requests.get(f"{base_url}/getalleventgroups", headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"❌ Gruplar alınamadı: {response.status_code}", file=sys.stderr)
            return []
        data = response.json()
        groups = data.get("valueList", [])
    except Exception as e:
        print(f"❌ Gruplar hatası: {e}", file=sys.stderr)
        return []

    print(f"🔍 {len(groups)} etkinlik grubu bulundu", file=sys.stderr)

    # 2. Her grup için detay isteği at
    for group in groups:
        group_id = group["id"]
        group_name = group["name"]
        print(f"📂 {group_name} grubu işleniyor...", file=sys.stderr)

        try:
            detail_response = requests.get(f"{base_url}/geteventgroupdetail/{group_id}", headers=headers, timeout=15)
            if detail_response.status_code != 200:
                print(f"⚠️  Detay alınamadı ({group_id}): {detail_response.status_code}", file=sys.stderr)
                continue

            detail_data = detail_response.json()
            event_list = detail_data.get("valueList", [])

            for item in event_list:
                try:
                    if not item.get("name") or not item.get("eventDate") or not item.get("venue"):
                        continue

                    raw_date = item["eventDate"]
                    date_part = raw_date.split("T")[0]  # "2025-09-04"
                    time_part = raw_date.split("T")[1][:5] if "T" in raw_date else "19:00"

                    venue = item["venue"]
                    lat = float(venue["latitude"]) if venue.get("latitude") else None
                    lng = float(venue["longitude"]) if venue.get("longitude") else None

                    events.append({
                        "ad": item["name"],
                        "tarih": date_part,
                        "saat": time_part,
                        "mekan_adi": venue["name"],
                        "link": f"https://passo.com.tr/etkinlik/{item['id']}",
                        "aciklama": item.get("shortDescription", f"{group_name} kapsamında"),
                        "latitude": lat,
                        "longitude": lng
                    })
                except Exception as e:
                    print(f"🟡 Etkinlik hatası: {e}", file=sys.stderr)
                    continue

            # Rate limit önlemi
            time.sleep(1)

        except Exception as e:
            print(f"❌ Detay isteği hatası ({group_id}): {e}", file=sys.stderr)
            continue

    print(f"{len(events)} etkinlik çekildi.", file=sys.stderr)
    return events

# 🚀 Ana işlem
if __name__ == "__main__":
    events = scrape_passo()
    json.dump(events, sys.stdout)
    sys.stdout.flush()
