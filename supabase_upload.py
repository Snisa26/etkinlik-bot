# supabase_upload.py
from supabase import create_client
import os
import sys
import json

# Supabase bilgileri (gizli anahtarlar ortamdan gelir)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def upload_to_supabase(events):
    """
    Supabase'e etkinlik listesini upsert (insert/update) olarak gönderir
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[HATA] Supabase URL veya KEY eksik!", file=sys.stderr)
        return False

    if not events:
        print("[UYARI] Gönderilecek etkinlik yok.", file=sys.stderr)
        return False

    try:
        print(f"[INFO] Supabase URL: {SUPABASE_URL}", file=sys.stderr)
        print(f"📤 Gönderilen etkinlik sayısı: {len(events)}", file=sys.stderr)
        
        for i, e in enumerate(events):
            print(f"   [{i+1}] {e.get('ad', 'Bilinmeyen')} @ {e.get('mekan_adi', 'Bilinmeyen')} → "
                  f"Lat: {e.get('latitude')}, Lng: {e.get('longitude')}", file=sys.stderr)

        # Supabase bağlantısı
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Veriyi upsert et
        response = supabase.table("etkinlikler").upsert(
            events,
            on_conflict="ad,tarih"
        ).execute()

        print(f"[BAŞARILI] Supabase'e {len(events)} etkinlik yüklendi.", file=sys.stderr)
        return True

    except Exception as e:
        print(f"[HATA] Supabase'e yükleme hatası: {e}", file=sys.stderr)
        return False


# 🚀 Ana işlem: stdin'den gelen JSON verisini al ve işle
if __name__ == "__main__":
    try:
        # stdin'den tüm veriyi al
        input_data = sys.stdin.read()
        
        # Boş kontrolü
        if not input_data.strip():
            print("⚠️  Hiç veri gelmedi (stdin boş).", file=sys.stderr)
            sys.exit(1)

        # Debug: Gelen ham veri
        print(f"🔍 Alınan ham veri uzunluğu: {len(input_data)} karakter", file=sys.stderr)
        
        # JSON parse et
        events = json.loads(input_data)
        
        if not isinstance(events, list):
            print(f"[HATA] Beklenen liste, gelen veri tipi: {type(events)}", file=sys.stderr)
            sys.exit(1)

        # Supabase'e yükle
        upload_to_supabase(events)

    except json.JSONDecodeError as e:
        print(f"[HATA] JSON çözme hatası: {e}", file=sys.stderr)
        print(f"📝 Geçersiz JSON içeriği: {repr(input_data[:200])}...", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[HATA] Beklenmeyen hata: {e}", file=sys.stderr)
        sys.exit(1)
