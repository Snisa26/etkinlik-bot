# scrape_passo.py
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from geocode import get_coordinates
import time
import sys
import json

def scrape_passo():
    url = "https://passo.com.tr/etkinlikler?sehir=Türkiye"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Sayfa açılamadı: {e}", file=sys.stderr)
        return []

    # Kodlama hatası olmaması için
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Etkinlik kartlarını bul
    event_items = soup.find_all("div", class_="event-card")  # Gerçek sınıf adı kontrol edilecek

    events = []

    for item in event_items[:10]:
        try:
            # Başlık
            title_elem = item.find("h3", class_="event-title")
            if not title_elem:
                title_elem = item.find("a", class_="event-link")  # Alternatif
            title = title_elem.get_text(strip=True) if title_elem else "Etkinlik İsmi Yok"

            # Tarih
            date_elem = item.find("div", class_="event-date")
            date_text = date_elem.get_text(strip=True) if date_elem else "Tarih Yok"
            # Basit tarih formatı: "12 Eylül" → "2025-09-12"
            match = re.search(r'(\d{1,2})\s+(\w+)', date_text)
            if match:
                day = match.group(1)
                month_tr = match.group(2)
                months = {"Ocak": "01", "Şubat": "02", "Mart": "03", "Nisan": "04",
                         "Mayıs": "05", "Haziran": "06", "Temmuz": "07", "Ağustos": "08",
                         "Eylül": "09", "Ekim": "10", "Kasım": "11", "Aralık": "12"}
                month = months.get(month_tr, "01")
                year = "2025"
                formatted_date = f"{year}-{month}-{day.zfill(2)}"
            else:
                formatted_date = "2025-01-01"

            # Mekan
            venue_elem = item.find("div", class_="event-location")
            venue = venue_elem.get_text(strip=True) if venue_elem else "Mekan Bilinmiyor"

            # Link
            link_elem = item.find("a", href=True)
            link = urljoin("https://passo.com.tr", link_elem['href']) if link_elem else "#"

            # 🗺️ Mekan adı düzeltme (Mapping)
            venue_mapping = {
                "Zorlu Center": "Zorlu Center",
                "Vodafone Park": "Vodafone Park",
                "Küçükçiftlik Parkı": "Küçükçiftlik Park",
                "Bostancı Gösteri Merkezi": "Bostancı Gösteri Merkezi",
                "Beşiktaş Stadyumu": "Vodafone Park",
                "Şükrü Saracoğlu": "Vodafone Park"
            }
            cleaned_venue = venue_mapping.get(venue, venue)

            # 🌍 KOORDİNAT AL
            print(f"🔍 {cleaned_venue} için koordinat aranıyor...", file=sys.stderr)
            lat, lng = get_coordinates(cleaned_venue)
            time.sleep(1)  # Rate limit

            events.append({
                "ad": title,
                "tarih": formatted_date,
                "saat": "19:00",  # Gerçek saat yok, tahmini
                "mekan_adi": venue,
                "link": link,
                "aciklama": f"{title} etkinliği için detay: {link}",
                "latitude": lat,
                "longitude": lng
            })
        except Exception as e:
            print(f"Veri hatası (passo): {e}", file=sys.stderr)
            continue

    print(f"{len(events)} etkinlik çekildi.", file=sys.stderr)
    return events

# 🚀 Ana işlem
if __name__ == "__main__":
    events = scrape_passo()
    json.dump(events, sys.stdout)
    sys.stdout.flush()