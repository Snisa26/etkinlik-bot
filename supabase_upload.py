# supabase_upload.py
from supabase import create_client
import os

SUPABASE_URL = "https://<senin-supabase-url>.supabase.co"
SUPABASE_KEY = "anon-key-buraya-yapıştır"

def upload_to_supabase(events):
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    try:
        response = supabase.table("etkinlikler").upsert(
            events,
            on_conflict=["ad", "tarih"]
        ).execute()

        print(f"Supabase'e {len(events)} etkinlik yüklendi.")
        return True
    except Exception as e:
        print(f"Supabase hatası: {e}")
        return False