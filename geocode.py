# geocode.py
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

# Nominatim (OpenStreetMap) için kullanıcı adı
geolocator = Nominatim(user_agent="etkinlik_bulucu")

def get_coordinates(venue_name):
    """
    Mekan adından koordinat alır
    """
    try:
        # Türkiye'de olduğundan emin olmak için "Türkiye" ekle
        location = geolocator.geocode(f"{venue_name}, Türkiye", timeout=10)
        
        if location:
            print(f"[KOORDİNAT] {venue_name} → {location.latitude}, {location.longitude}")
            return round(location.latitude, 6), round(location.longitude, 6)
        else:
            print(f"[UYARI] {venue_name} bulunamadı")
            return None, None
            
    except GeocoderTimedOut:
        print(f"[HATA] Zaman aşımı: {venue_name}")
        return None, None
    except GeocoderServiceError as e:
        print(f"[HATA] Servis hatası: {e}")
        return None, None
    except Exception as e:
        print(f"[HATA] Beklenmeyen hata: {e}")
        return None, None

# Test
if __name__ == "__main__":
    lat, lng = get_coordinates("Zorlu Center")
    print(f"Sonuç: {lat}, {lng}")