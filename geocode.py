# geocode.py
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

geolocator = Nominatim(user_agent="etkinlik_bulucu")

def get_coordinates(venue_name):
    print(f"🔍 KOORDİNAT ARANIYOR: {venue_name}")
    try:
        location = geolocator.geocode(f"{venue_name}, Türkiye", timeout=10)
        if location:
            print(f"✅ BULUNDU: {venue_name} → {location.latitude}, {location.longitude}")
            return round(location.latitude, 6), round(location.longitude, 6)
        else:
            print(f"❌ BULUNAMADI: {venue_name}")
            return None, None
    except GeocoderTimedOut:
        print(f"⏰ ZAMAN AŞIMI: {venue_name}")
        return None, None
    except GeocoderServiceError as e:
        print(f"🔧 SERVİS HATASI: {e}")
        return None, None
    except Exception as e:
        print(f"💥 BEKLENMEYEN HATA: {e}")
        return None, None
