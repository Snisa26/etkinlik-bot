# supabase_upload.py
from supabase import create_client
import os
import sys

# Supabase bilgileri (gizli anahtarlar ortamdan gelir)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def upload_to_supabase(events):
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[HATA] Supabase URL veya KEY eksik!")
        return False

    try:
        print(f"[INFO] Supabase URL: {SUPABASE_URL}")
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = supabase.table("etkinlikler").upsert(
            events,
            on_conflict=["ad", "tarih"]
        ).execute()

        print(f"[BAŞARILI] Supabase'e {len(events)} etkinlik yüklendi.")
        return True
    except Exception as e:
        print(f"[HATA] Supabase'e yükleme hatası: {e}")
        return False

# Komut satırından çalıştırılıyorsa
if __name__ == "__main__":
    # Test verisi
    test_events = [
        {
            "ad": "Test Etkinlik",
            "tarih": "2025-09-04",
            "saat": "19:00",
            "mekan_adi": "Zorlu Center",
            "link": "https://test.com",
            "aciklama": "Bu bir test etkinliğidir",
            "latitude": None,
            "longitude": None
        }
    ]
    upload_to_supabase(test_events)
