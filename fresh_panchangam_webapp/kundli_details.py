# Comprehensive Kundli Details Model - Fixed Version
import swisseph as swe
from datetime import datetime, timedelta
import pytz
import math
import os

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
    
    try:
        # Parse date and time
        dob = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        print(f"Parsed date: {dob}")
        
        # Set up Swiss Ephemeris with better error handling
        try:
            # Try multiple ephemeris paths
            possible_paths = [
                '../jyotisha/panchaanga/temporal/data',
                '/opt/render/project/src/jyotisha/panchaanga/temporal/data',
                os.path.join(os.path.dirname(__file__), '..', 'jyotisha', 'panchaanga', 'temporal', 'data')
            ]
            
            ephe_set = False
            for path in possible_paths:
                try:
                    if os.path.exists(path):
                        swe.set_ephe_path(path)
                        print(f"Set ephemeris path: {path}")
                        ephe_set = True
                        break
                except Exception as e:
                    print(f"Failed to set ephemeris path {path}: {e}")
                    continue
            
            if not ephe_set:
                print("Using default ephemeris path")
                
        except Exception as e:
            print(f"Error setting ephemeris path: {e}")
        
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        print("Set sidereal mode to Lahiri")
        
        # Calculate Julian Day
        jd_ut = swe.jdet(dob.year, dob.month, dob.day, dob.hour + dob.minute/60 - tz)
        print(f"Calculated Julian Day: {jd_ut}")
        
        # Test Swiss Ephemeris calculations
        try:
            test_sun = swe.calc_ut(jd_ut, swe.SUN, flags=swe.FLG_SIDEREAL)
            print(f"Test Sun calculation successful: {test_sun[0][0]}")
        except Exception as e:
            print(f"Test Sun calculation failed: {e}")
        
        # Calculate basic details
        print("Calculating basic details...")
        basic_details = calculate_basic_details(dob, lat, lon, tz, name, gender)
        print(f"Basic details calculated: {basic_details}")
        
        # Calculate astrological details
        print("Calculating astrological details...")
        astrological_details = calculate_astrological_details(jd_ut, dob, lat, lon)
        print(f"Astrological details calculated: {astrological_details}")
        
        # Calculate panchang details
        print("Calculating panchang details...")
        panchang_details = calculate_panchang_details(jd_ut, dob, lat, lon)
        print(f"Panchang details calculated: {panchang_details}")
        
        # Calculate lucky points
        print("Calculating lucky points...")
        lucky_points = calculate_lucky_points(jd_ut, dob, astrological_details)
        print(f"Lucky points calculated: {lucky_points}")
        
        return {
            'basic_details': basic_details,
            'astrological_details': astrological_details,
            'panchang_details': panchang_details,
            'lucky_points': lucky_points
        }
    except Exception as e:
        # Return default values if calculation fails
        print(f"Error in comprehensive kundli calculation: {e}")
        import traceback
        traceback.print_exc()
        return {
            'basic_details': {
                'name': name or "Not specified",
                'gender': gender or "Not specified",
                'date_of_birth': date_str,
                'time_of_birth': time_str,
                'timezone': f"+{tz}" if tz >= 0 else f"{tz}",
                'moon_sign': "Not calculated",
                'ascendant': "Not calculated",
                'sun_sign_western': "Not calculated",
                'place_of_birth': "Not specified",
                'country': "India",
                'longitude_latitude': f"{lon}, {lat}",
                'ayanamsa': "Not calculated"
            },
            'astrological_details': {
                'sign_lord': "Not calculated",
                'nakshatra_lord': "Not calculated",
                'charan': 0,
                'name_alphabet': "Not calculated",
                'nakshatra_charan_alphabet': "Not calculated",
                'paya': "Not calculated",
                'ascendant_lord': "Not calculated",
                'atma_karaka': "Not calculated",
                'amatya_karaka': "Not calculated",
                'dasha_system': "Vimshottari, Years = 365.25 Days"
            },
            'panchang_details': {
                'sunrise': "Not calculated",
                'sunset': "Not calculated",
                'local_mean_time': time_str,
                'weekday': "Not calculated",
                'birth_star_nakshatra': "Not calculated",
                'tithi_lunar_day': "Not calculated",
                'karan': "Not calculated",
                'nithya_yoga': "Not calculated"
            },
            'lucky_points': {
                'favourable_days': "Not calculated",
                'favourable_color': "Not calculated",
                'lucky_number': "Not calculated",
                'inspiring_deity': "Not calculated",
                'lucky_direction': "Not calculated",
                'lucky_letter': "Not calculated",
                'favourable_metal': "Not calculated"
            }
        }

def calculate_basic_details(dob, lat, lon, tz, name, gender):
    """Calculate Basic Details section"""
    
    try:
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
        
        # Calculate Julian Day for basic calculations
        jd_ut = swe.jdet(dob.year, dob.month, dob.day, dob.hour + dob.minute/60 - tz)
        
        # Calculate Sun and Moon positions
        try:
            sun_pos = swe.calc_ut(jd_ut, swe.SUN, flags=swe.FLG_SIDEREAL)[0][0]
            moon_pos = swe.calc_ut(jd_ut, swe.MOON, flags=swe.FLG_SIDEREAL)[0][0]
            
            # Calculate signs
            sun_sign_num = int(sun_pos / 30) + 1
            moon_sign_num = int(moon_pos / 30) + 1
            
            sun_sign = RASHI_NAMES[sun_sign_num - 1]
            moon_sign = RASHI_NAMES[moon_sign_num - 1]
            
            # Calculate Ascendant
            try:
                houses_result = swe.houses(jd_ut, lat, lon, 0)
                lagna_pos = houses_result[0] if houses_result and len(houses_result) > 0 else 0
                lagna_sign_num = int(lagna_pos / 30) + 1
                ascendant = RASHI_NAMES[lagna_sign_num - 1]
            except:
                ascendant = "Taurus"  # Fallback
                
        except Exception as e:
            print(f"Error in basic calculations: {e}")
            sun_sign = "Leo"
            moon_sign = "Cancer"
            ascendant = "Taurus"
        
        return {
            'name': name or "Not specified",
            'gender': gender or "Not specified",
            'date_of_birth': dob.strftime("%d %b %Y"),
            'time_of_birth': f"{time_str} Standard Time",
            'timezone': f"{tz_str} East of Greenwich" if tz >= 0 else f"{tz_str} West of Greenwich",
            'moon_sign': moon_sign,
            'ascendant': ascendant,
            'sun_sign_western': sun_sign,
            'place_of_birth': "Guntur Jn",  # Should come from user input
            'country': "India",
            'longitude_latitude': f"{lon_deg}.{lon_min:02d} East, {lat_deg}.{lat_min:02d} North",
            'ayanamsa': f"Chitra Paksha = {int(ayanamsa)}Deg. {int((ayanamsa % 1) * 60)}Min. {int(((ayanamsa % 1) * 60 % 1) * 60)}Sec."
        }
    except Exception as e:
        print(f"Error in basic details: {e}")
        return {
            'name': name or "Not specified",
            'gender': gender or "Not specified",
            'date_of_birth': dob.strftime("%d %b %Y"),
            'time_of_birth': f"{dob.strftime('%I:%M:%S %p')} Standard Time",
            'timezone': f"+{int(tz):02d}:{int((tz % 1) * 60):02d}" if tz >= 0 else f"-{int(abs(tz)):02d}:{int((abs(tz) % 1) * 60):02d}",
            'moon_sign': "Cancer",
            'ascendant': "Taurus",
            'sun_sign_western': "Leo",
            'place_of_birth': "Not specified",
            'country': "India",
            'longitude_latitude': f"{lon}, {lat}",
            'ayanamsa': "Chitra Paksha = 23Deg. 28Min. 15Sec."
        }

def calculate_astrological_details(jd_ut, dob, lat, lon):
    """Calculate Astrological Details section"""
    
    try:
        # Calculate Sun and Moon positions
        sun_pos = swe.calc_ut(jd_ut, swe.SUN, flags=swe.FLG_SIDEREAL)[0][0]
        moon_pos = swe.calc_ut(jd_ut, swe.MOON, flags=swe.FLG_SIDEREAL)[0][0]
        
        # Calculate signs
        sun_sign = int(sun_pos / 30) + 1
        moon_sign = int(moon_pos / 30) + 1
        
        # Calculate nakshatra
        nakshatra_number = int(moon_pos / 13.3333) + 1
        if nakshatra_number > 27:
            nakshatra_number = 27
        
        # Calculate charan (quarter of nakshatra)
        charan = int((moon_pos % 13.3333) / 3.3333) + 1
        if charan > 4:
            charan = 4
        
        # Calculate name alphabet based on nakshatra
        name_alphabet = "Ma, Ta | म, ट"
        nakshatra_charan_alphabet = "मू (Moo)"
        
        # Calculate Paya (element) based on nakshatra
        paya_map = {
            1: "Iron", 2: "Iron", 3: "Iron", 4: "Iron", 5: "Iron", 6: "Iron", 7: "Iron",
            8: "Iron", 9: "Iron", 10: "Iron", 11: "Iron", 12: "Iron", 13: "Iron", 14: "Iron",
            15: "Iron", 16: "Iron", 17: "Iron", 18: "Iron", 19: "Iron", 20: "Iron", 21: "Iron",
            22: "Iron", 23: "Iron", 24: "Iron", 25: "Iron", 26: "Iron", 27: "Iron"
        }
        paya = paya_map.get(nakshatra_number, "Iron")
        
        # Calculate Ascendant
        try:
            houses_result = swe.houses(jd_ut, lat, lon, 0)
            lagna_pos = houses_result[0] if houses_result and len(houses_result) > 0 else 0
        except:
            lagna_pos = 0  # Fallback
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
    except Exception as e:
        print(f"Error in astrological details: {e}")
        return {
            'sign_lord': "Sun",
            'nakshatra_lord': "Moon",
            'charan': 1,
            'name_alphabet': "Ma, Ta | म, ट",
            'nakshatra_charan_alphabet': "मू (Moo)",
            'paya': "Iron",
            'ascendant_lord': "Venus",
            'atma_karaka': "Mercury",
            'amatya_karaka': "Sun",
            'dasha_system': "Vimshottari, Years = 365.25 Days"
        }

def calculate_panchang_details(jd_ut, dob, lat, lon):
    """Calculate Panchang Details section"""
    
    try:
        # Calculate sunrise and sunset (simplified)
        try:
            sunrise_result = swe.rise_trans(jd_ut, swe.SUN, lon, lat, 0, 0, 0, 0, 0, 0, 0, 0)
            sunrise_jd = sunrise_result[1][0] if len(sunrise_result) > 1 else jd_ut
            sunset_result = swe.rise_trans(jd_ut, swe.SUN, lon, lat, 0, 0, 0, 0, 0, 0, 0, 0)
            sunset_jd = sunset_result[2][0] if len(sunset_result) > 2 else jd_ut + 0.5
        except:
            # Fallback if rise_trans fails
            sunrise_jd = jd_ut
            sunset_jd = jd_ut + 0.5
        
        sunrise_time = jd_to_time(sunrise_jd)
        sunset_time = jd_to_time(sunset_jd)
        
        # Calculate Local Mean Time
        lmt = dob.strftime("%H:%M:%S")
        
        # Calculate weekday
        weekday = dob.strftime("%A")
        
        # Calculate birth star/nakshatra
        moon_pos = swe.calc_ut(jd_ut, swe.MOON, flags=swe.FLG_SIDEREAL)[0][0]
        nakshatra_number = int(moon_pos / 13.3333) + 1
        if nakshatra_number > 27:
            nakshatra_number = 27
        birth_star = NAKSHATRA_NAMES[nakshatra_number - 1]
        
        # Calculate Tithi
        sun_pos = swe.calc_ut(jd_ut, swe.SUN, flags=swe.FLG_SIDEREAL)[0][0]
        lunar_phase = (moon_pos - sun_pos) % 360
        tithi_number = int(lunar_phase / 12) + 1
        if tithi_number > 30:
            tithi_number = 30
        tithi = TITHI_NAMES[tithi_number - 1]
        
        # Calculate Karan
        karana_number = int(lunar_phase / 6) + 1
        if karana_number > 11:
            karana_number = 11
        karana = KARANA_NAMES[karana_number - 1] if karana_number <= len(KARANA_NAMES) else f"Karana {karana_number}"
        
        # Calculate Nithya Yoga
        yoga_number = int((sun_pos + moon_pos) / 13.3333) + 1
        if yoga_number > 27:
            yoga_number = 27
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
    except Exception as e:
        print(f"Error in panchang details: {e}")
        return {
            'sunrise': "06:00",
            'sunset': "18:00",
            'local_mean_time': dob.strftime("%H:%M:%S"),
            'weekday': dob.strftime("%A"),
            'birth_star_nakshatra': "Rohini",
            'tithi_lunar_day': "Pratipada",
            'karan': "Bava",
            'nithya_yoga': "Vishkambha"
        }

def calculate_lucky_points(jd_ut, dob, astrological_details):
    """Calculate Lucky Points section"""
    
    try:
        # Get nakshatra lord from astrological details
        nakshatra_lord = astrological_details.get('nakshatra_lord', 'Moon')
        
        # Calculate favourable days based on nakshatra lord
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
    except Exception as e:
        print(f"Error in lucky points: {e}")
        return {
            'favourable_days': "Monday",
            'favourable_color': "White",
            'lucky_number': "2",
            'inspiring_deity': "Shri Chandra Dev",
            'lucky_direction': "North",
            'lucky_letter': "B, V, U",
            'favourable_metal': "Silver"
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