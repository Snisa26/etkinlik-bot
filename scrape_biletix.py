# scrape_biletix.py
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from geocode import get_coordinates
import time
import sys
import json  # ✅ En başa alındı

def scrape_biletix():
    # 🔗 URL'deki gereksiz boşluklar temizlendi
    url = "https://www.biletix.com/anasayfa/TURKIYE/tr"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Sayfa açılamadı: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    events = []

    event_items = soup.find_all("div", class_="event-item")

    # 🗺️ Mekan adı düzeltme (Mapping)
    venue_mapping = {
        "Zorlu Center Sahnesi": "Zorlu Center",
        "Zorlu": "Zorlu Center",
        "Zorlu Center": "Zorlu Center",
        "Zorlu Sahnesi": "Zorlu Center",
        "Vodafone Park": "Vodafone Park",
        "Küçükçiftlik Park": "Küçükçiftlik Parkı",
        "Bostancı Show Center": "Bostancı Gösteri Merkezi",
        "Maslak Arkadia": "Arkadia Alışveriş Merkezi",
        "İstinye Park": "İstinye Park",
        "Forum İstanbul": "Forum İstanbul",
        "Cevahir Sahnesi": "Cevahir Hotel & Convention Center",
        "Zorlu Pembe": "Zorlu Center",
        "Pembe Sahne": "Zorlu Center",
        "Sahne 1": "Zorlu Center",
        "Sahne 2": "Zorlu Center",
        "Kültür Merkezi": "İstanbul Kültür Merkezi",
        "Sanat Merkezi": "İstanbul Sanat Merkezi"
    }

    for item in event_items[:10]:
        try:
            title_elem = item.find("h3", class_="event-title")
            date_elem = item.find("span", class_="event-date")
            venue_elem = item.find("span", class_="event-venue")
            link_elem = item.find("a", href=True)

            if not all([title_elem, date_elem, venue_elem, link_elem]):
                continue

            title = title_elem.get_text(strip=True)
            date_text = date_elem.get_text(strip=True)
            venue = venue_elem.get_text(strip=True)
            # 🔗 Link URL'sinde gereksiz boşluk temizlendi
            link = urljoin("https://www.biletix.com", link_elem['href'])

            # 📅 Tarih formatı
            match = re.search(r'(\d{1,2})\s+(\w{3})', date_text)
            if match:
                day = match.group(1)
                month_tr = match.group(2)
                months = {
                    "Oca": "01", "Şub": "02", "Mar": "03", "Nis": "04",
                    "May": "05", "Haz": "06", "Tem": "07", "Ağu": "08",
                    "Eyl": "09", "Eki": "10", "Kas": "11", "Ara": "12"
                }
                month = months.get(month_tr, "01")
                year = "2025"
                formatted_date = f"{year}-{month}-{day.zfill(2)}"
            else:
                formatted_date = "2025-01-01"

            # 🗺️ Mekan adı düzelt
            cleaned_venue = venue_mapping.get(venue, venue)

            # 🌍 KOORDİNAT AL
            print(f"🔍 {cleaned_venue} için koordinat aranıyor...", file=sys.stderr)
            lat, lng = get_coordinates(cleaned_venue)
            time.sleep(1)  # Rate limit önlemi

            events.append({
                "ad": title,
                "tarih": formatted_date,
                "saat": "19:00",
                "mekan_adi": venue,
                "link": link,
                "aciklama": f"{title} etkinliği için detay: {link}",
                "latitude": lat,
                "longitude": lng
            })
        except Exception as e:
            print(f"Veri hatası: {e}", file=sys.stderr)
            continue

    print(f"{len(events)} etkinlik çekildi.", file=sys.stderr)
    return events

# 🚀 Ana işlem: stdout'a JSON verisi yaz
if __name__ == "__main__":
    events = scrape_biletix()
    json.dump(events, sys.stdout)
    sys.stdout.flush()  # ✅ Verinin hemen gönderilmesini sağlar
