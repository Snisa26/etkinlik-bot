# supabase_upload.py
from supabase import create_client
import os
import sys
import json

# Supabase bilgileri (gizli anahtarlar ortamdan gelir)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def upload_to_supabase(events):
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[HATA] Supabase URL veya KEY eksik!")
        return False

    try:
        print(f"[INFO] Supabase URL: {SUPABASE_URL}")
        print(f"📤 Gönderilen etkinlik sayısı: {len(events)}")
        for e in events:
            print(f"   - {e['ad']} @ {e['mekan_adi']} → {e['latitude']}, {e['longitude']}")

        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = supabase.table("etkinlikler").upsert(
            events,
            on_conflict="ad,tarih"
        ).execute()

        print(f"[BAŞARILI] Supabase'e {len(events)} etkinlik yüklendi.")
        return True
    except Exception as e:
        print(f"[HATA] Supabase'e yükleme hatası: {e}")
        return False

# Komut satırından çalıştırılıyorsa ve argüman varsa
if __name__ == "__main__":
    try:
        # stdin'den gelen veriyi al (scrape_biletix.py'den)
        input_data = sys.stdin.read()
        if input_data.strip():
            events = json.loads(input_data)
            upload_to_supabase(events)
        else:
            # Hiç veri yoksa test verisi ile çalış
            print("⚠️  Hiç veri gelmedi, test verisiyle denenecek.")
            test_events = [
                {
                    "ad": "Test Etkinlik",
                    "tarih": "2025-09-04",
                    "saat": "19:00",
                    "mekan_adi": "Zorlu Center",
                    "link": "https://test.com",
                    "aciklama": "Bu bir test etkinliğidir",
                    "latitude": 41.066471,
                    "longitude": 29.018046
                }
            ]
            upload_to_supabase(test_events)
    except Exception as e:
        print(f"❌ Ana süreç hatası: {e}")
