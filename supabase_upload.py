# supabase_upload.py
from supabase import create_client
import os
import sys
import json

# Supabase bilgileri
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

# 🚀 Ana işlem: stdin'den gelen veriyi al
if __name__ == "__main__":
    try:
        # stdin'den JSON verisi al
        input_data = sys.stdin.read()
        if input_data.strip():
            events = json.loads(input_data)
            upload_to_supabase(events)
        else:
            print("⚠️  Hiç veri gelmedi.")
    except Exception as e:
        print(f"❌ Veri işleme hatası: {e}")
        # Hata olsa bile test değil, sadece hata ver
