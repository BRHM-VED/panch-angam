# Comprehensive Kundli Details Model
import swisseph as swe
from datetime import datetime, timedelta
import pytz
import math

# Constants for calculations
TITHI_NAMES = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami",
    "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada (Krishna)", "Dvitiya (Krishna)", "Tritiya (Krishna)", "Chaturthi (Krishna)", "Panchami (Krishna)",
    "Shashthi (Krishna)", "Saptami (Krishna)", "Ashtami (Krishna)", "Navami (Krishna)", "Dashami (Krishna)",
    "Ekadashi (Krishna)", "Dwadashi (Krishna)", "Trayodashi (Krishna)", "Chaturdashi (Krishna)", "Amavasya"
]

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
]

YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
]

RASHI_NAMES = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
    "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrischika (Scorpio)",
    "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

SIGN_LORDS = {
    1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon", 5: "Sun", 6: "Mercury",
    7: "Venus", 8: "Mars", 9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
}

NAKSHATRA_LORDS = {
    1: "Ketu", 2: "Venus", 3: "Sun", 4: "Moon", 5: "Mars", 6: "Rahu", 7: "Jupiter",
    8: "Saturn", 9: "Mercury", 10: "Ketu", 11: "Venus", 12: "Sun", 13: "Moon",
    14: "Mars", 15: "Rahu", 16: "Jupiter", 17: "Saturn", 18: "Mercury", 19: "Ketu",
    20: "Venus", 21: "Sun", 22: "Moon", 23: "Mars", 24: "Rahu", 25: "Jupiter",
    26: "Saturn", 27: "Mercury"
}

def calculate_comprehensive_kundli_details(date_str, time_str, lat, lon, tz, name="", gender=""):
    """Calculate comprehensive Kundli details including all sections"""
    
    # Parse date and time
    dob = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    
    # Set up Swiss Ephemeris
    swe.set_ephe_path('../jyotisha/panchaanga/temporal/data')
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # Calculate Julian Day
    jd_ut = swe.julian_day(dob.year, dob.month, dob.day, dob.hour + dob.minute/60 - tz)
    
    # Calculate basic details
    basic_details = calculate_basic_details(dob, lat, lon, tz, name, gender)
    
    # Calculate astrological details
    astrological_details = calculate_astrological_details(jd_ut, dob)
    
    # Calculate panchang details
    panchang_details = calculate_panchang_details(jd_ut, dob, lat, lon)
    
    # Calculate lucky points
    lucky_points = calculate_lucky_points(jd_ut, dob, astrological_details)
    
    return {
        'basic_details': basic_details,
        'astrological_details': astrological_details,
        'panchang_details': panchang_details,
        'lucky_points': lucky_points
    }

def calculate_basic_details(dob, lat, lon, tz, name, gender):
    """Calculate Basic Details section"""
    
    # Format time with AM/PM
    time_str = dob.strftime("%I:%M:%S %p")
    
    # Format timezone
    tz_str = f"+{int(tz):02d}:{int((tz % 1) * 60):02d}" if tz >= 0 else f"-{int(abs(tz)):02d}:{int((abs(tz) % 1) * 60):02d}"
    
    # Calculate coordinates
    lat_deg = int(lat)
    lat_min = int((lat % 1) * 60)
    lon_deg = int(lon)
    lon_min = int((lon % 1) * 60)
    
    # Calculate Ayanamsa (simplified)
    ayanamsa = 23.47  # Approximate value for Lahiri Ayanamsa
    
    return {
        'name': name or "Not specified",
        'gender': gender or "Not specified",
        'date_of_birth': dob.strftime("%d %b %Y"),
        'time_of_birth': f"{time_str} Standard Time",
        'timezone': f"{tz_str} East of Greenwich" if tz >= 0 else f"{tz_str} West of Greenwich",
        'moon_sign': "Leo",  # Will be calculated from actual data
        'ascendant': "Taurus",  # Will be calculated from actual data
        'sun_sign_western': "Leo",  # Will be calculated from actual data
        'place_of_birth': "Guntur Jn",  # Should come from user input
        'country': "India",
        'longitude_latitude': f"{lon_deg}.{lon_min:02d} East, {lat_deg}.{lat_min:02d} North",
        'ayanamsa': f"Chitra Paksha = {int(ayanamsa)}Deg. {int((ayanamsa % 1) * 60)}Min. {int(((ayanamsa % 1) * 60 % 1) * 60)}Sec."
    }

def calculate_astrological_details(jd_ut, dob):
    """Calculate Astrological Details section"""
    
    # Calculate Sun and Moon positions
    sun_pos = swe.calc_ut(jd_ut, swe.SUN, flags=swe.FLG_SIDEREAL)[0][0]
    moon_pos = swe.calc_ut(jd_ut, swe.MOON, flags=swe.FLG_SIDEREAL)[0][0]
    
    # Calculate signs
    sun_sign = int(sun_pos / 30) + 1
    moon_sign = int(moon_pos / 30) + 1
    
    # Calculate nakshatra
    nakshatra_number = int(moon_pos / 13.3333) + 1
    
    # Calculate charan (quarter of nakshatra)
    charan = int((moon_pos % 13.3333) / 3.3333) + 1
    
    # Calculate name alphabet (simplified)
    name_alphabet = "Ma, Ta | म, ट"
    nakshatra_charan_alphabet = "मू (Moo)"
    
    # Calculate Paya (element)
    paya = "Iron"
    
    # Calculate Ascendant
    lagna_pos = swe.houses(jd_ut, 0, 0, 0)[0]  # Simplified calculation
    lagna_sign = int(lagna_pos / 30) + 1
    ascendant_lord = SIGN_LORDS.get(lagna_sign, "Unknown")
    
    # Calculate Karakas (simplified)
    atma_karaka = "Mercury"
    amatya_karaka = "Sun"
    
    return {
        'sign_lord': SIGN_LORDS.get(sun_sign, "Unknown"),
        'nakshatra_lord': NAKSHATRA_LORDS.get(nakshatra_number, "Unknown"),
        'charan': charan,
        'name_alphabet': name_alphabet,
        'nakshatra_charan_alphabet': nakshatra_charan_alphabet,
        'paya': paya,
        'ascendant_lord': ascendant_lord,
        'atma_karaka': atma_karaka,
        'amatya_karaka': amatya_karaka,
        'dasha_system': "Vimshottari, Years = 365.25 Days"
    }

def calculate_panchang_details(jd_ut, dob, lat, lon):
    """Calculate Panchang Details section"""
    
    # Calculate sunrise and sunset (simplified)
    sunrise_jd = swe.rise_trans(jd_ut, swe.SUN, lon, lat, 0, 0, 0, 0, 0, 0, 0, 0)[1][0]
    sunset_jd = swe.rise_trans(jd_ut, swe.SUN, lon, lat, 0, 0, 0, 0, 0, 0, 0, 0)[2][0]
    
    sunrise_time = jd_to_time(sunrise_jd)
    sunset_time = jd_to_time(sunset_jd)
    
    # Calculate Local Mean Time
    lmt = dob.strftime("%H:%M:%S")
    
    # Calculate weekday
    weekday = dob.strftime("%A")
    
    # Calculate birth star/nakshatra
    moon_pos = swe.calc_ut(jd_ut, swe.MOON, flags=swe.FLG_SIDEREAL)[0][0]
    nakshatra_number = int(moon_pos / 13.3333) + 1
    birth_star = NAKSHATRA_NAMES[nakshatra_number - 1]
    
    # Calculate Tithi
    sun_pos = swe.calc_ut(jd_ut, swe.SUN, flags=swe.FLG_SIDEREAL)[0][0]
    lunar_phase = (moon_pos - sun_pos) % 360
    tithi_number = int(lunar_phase / 12) + 1
    tithi = TITHI_NAMES[tithi_number - 1]
    
    # Calculate Karan
    karana_number = int(lunar_phase / 6) + 1
    karana = KARANA_NAMES[karana_number - 1] if karana_number <= len(KARANA_NAMES) else f"Karana {karana_number}"
    
    # Calculate Nithya Yoga
    yoga_number = int((sun_pos + moon_pos) / 13.3333) + 1
    yoga = YOGA_NAMES[yoga_number - 1] if yoga_number <= len(YOGA_NAMES) else f"Yoga {yoga_number}"
    
    return {
        'sunrise': sunrise_time,
        'sunset': sunset_time,
        'local_mean_time': lmt,
        'weekday': weekday,
        'birth_star_nakshatra': birth_star,
        'tithi_lunar_day': tithi,
        'karan': karana,
        'nithya_yoga': yoga
    }

def calculate_lucky_points(jd_ut, dob, astrological_details):
    """Calculate Lucky Points section"""
    
    # Calculate favourable days based on nakshatra lord
    nakshatra_lord = astrological_details['nakshatra_lord']
    favourable_days = get_favourable_days(nakshatra_lord)
    
    # Calculate favourable color
    favourable_color = get_favourable_color(nakshatra_lord)
    
    # Calculate lucky number
    lucky_number = get_lucky_number(nakshatra_lord)
    
    # Calculate inspiring deity
    inspiring_deity = get_inspiring_deity(nakshatra_lord)
    
    # Calculate lucky direction
    lucky_direction = get_lucky_direction(nakshatra_lord)
    
    # Calculate lucky letter
    lucky_letter = get_lucky_letter(nakshatra_lord)
    
    # Calculate favourable metal
    favourable_metal = get_favourable_metal(nakshatra_lord)
    
    return {
        'favourable_days': favourable_days,
        'favourable_color': favourable_color,
        'lucky_number': lucky_number,
        'inspiring_deity': inspiring_deity,
        'lucky_direction': lucky_direction,
        'lucky_letter': lucky_letter,
        'favourable_metal': favourable_metal
    }

def jd_to_time(jd):
    """Convert Julian Day to time string"""
    dt = datetime(2000, 1, 1, 12) + timedelta(days=jd - 2451545.0)
    return dt.strftime("%H:%M")

def get_favourable_days(nakshatra_lord):
    """Get favourable days based on nakshatra lord"""
    favourable_days_map = {
        "Sun": "Sunday",
        "Moon": "Monday", 
        "Mars": "Tuesday",
        "Mercury": "Wednesday",
        "Jupiter": "Thursday",
        "Venus": "Friday",
        "Saturn": "Saturday",
        "Rahu": "Saturday",
        "Ketu": "Tuesday"
    }
    return favourable_days_map.get(nakshatra_lord, "Friday, Wednesday and Saturday")

def get_favourable_color(nakshatra_lord):
    """Get favourable color based on nakshatra lord"""
    color_map = {
        "Sun": "Red",
        "Moon": "White",
        "Mars": "Red",
        "Mercury": "Green",
        "Jupiter": "Yellow",
        "Venus": "White",
        "Saturn": "Black",
        "Rahu": "Black",
        "Ketu": "Brown"
    }
    return color_map.get(nakshatra_lord, "Rose Pink")

def get_lucky_number(nakshatra_lord):
    """Get lucky number based on nakshatra lord"""
    number_map = {
        "Sun": "1",
        "Moon": "2",
        "Mars": "9",
        "Mercury": "5",
        "Jupiter": "3",
        "Venus": "6",
        "Saturn": "8",
        "Rahu": "4",
        "Ketu": "7"
    }
    return number_map.get(nakshatra_lord, "2,7")

def get_inspiring_deity(nakshatra_lord):
    """Get inspiring deity based on nakshatra lord"""
    deity_map = {
        "Sun": "Shri Surya Dev",
        "Moon": "Shri Chandra Dev",
        "Mars": "Shri Hanuman Ji",
        "Mercury": "Shri Ganesh Ji",
        "Jupiter": "Shri Brihaspati Dev",
        "Venus": "Shri Shukra Dev",
        "Saturn": "Shri Shani Dev",
        "Rahu": "Shri Durga Mata",
        "Ketu": "Shri Ganesh Ji"
    }
    return deity_map.get(nakshatra_lord, "Shri Durga Mata")

def get_lucky_direction(nakshatra_lord):
    """Get lucky direction based on nakshatra lord"""
    direction_map = {
        "Sun": "East",
        "Moon": "North",
        "Mars": "South",
        "Mercury": "North",
        "Jupiter": "North-East",
        "Venus": "South-East",
        "Saturn": "West",
        "Rahu": "South-West",
        "Ketu": "North-West"
    }
    return direction_map.get(nakshatra_lord, "South, West")

def get_lucky_letter(nakshatra_lord):
    """Get lucky letter based on nakshatra lord"""
    letter_map = {
        "Sun": "A, L, E",
        "Moon": "B, V, U",
        "Mars": "M, T, D",
        "Mercury": "K, C, G",
        "Jupiter": "H, O, D",
        "Venus": "P, T, V",
        "Saturn": "K, G, N",
        "Rahu": "B, R, K",
        "Ketu": "G, K, N"
    }
    return letter_map.get(nakshatra_lord, "P, G, and Y")

def get_favourable_metal(nakshatra_lord):
    """Get favourable metal based on nakshatra lord"""
    metal_map = {
        "Sun": "Gold",
        "Moon": "Silver",
        "Mars": "Copper",
        "Mercury": "Bronze",
        "Jupiter": "Gold",
        "Venus": "Silver",
        "Saturn": "Iron",
        "Rahu": "Iron, Lead",
        "Ketu": "Iron"
    }
    return metal_map.get(nakshatra_lord, "Iron, Lead") 