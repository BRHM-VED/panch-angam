"""
Astrology Basics Module
Extracts and processes Basic and Astrological Details from Kundli data
"""

import swisseph as swe
from datetime import datetime
from typing import Dict, List, Tuple

# Zodiac signs and their lords
ZODIAC_SIGNS = {
    "Mesha (Aries)": "Mars",
    "Vrishabha (Taurus)": "Venus", 
    "Mithuna (Gemini)": "Mercury",
    "Karka (Cancer)": "Moon",
    "Simha (Leo)": "Sun",
    "Kanya (Virgo)": "Mercury",
    "Tula (Libra)": "Venus",
    "Vrischika (Scorpio)": "Mars",
    "Dhanu (Sagittarius)": "Jupiter",
    "Makara (Capricorn)": "Saturn",
    "Kumbha (Aquarius)": "Saturn",
    "Meena (Pisces)": "Jupiter"
}

# Nakshatra lords mapping
NAKSHATRA_LORDS = {
    1: "Ketu", 2: "Venus", 3: "Sun", 4: "Moon", 5: "Mars", 6: "Rahu", 7: "Jupiter",
    8: "Saturn", 9: "Mercury", 10: "Ketu", 11: "Venus", 12: "Sun", 13: "Moon",
    14: "Mars", 15: "Rahu", 16: "Jupiter", 17: "Saturn", 18: "Mercury", 19: "Ketu",
    20: "Venus", 21: "Sun", 22: "Moon", 23: "Mars", 24: "Rahu", 25: "Jupiter",
    26: "Saturn", 27: "Mercury"
}

# Planet mapping for calculations
PLANET_CODES = {
    'Sun': swe.SUN,
    'Moon': swe.MOON, 
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu (Mean)': swe.MEAN_NODE
}

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

def get_favourable_days(nakshatra_lord: str) -> str:
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

def get_favourable_color(nakshatra_lord: str) -> str:
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

def get_lucky_number(nakshatra_lord: str) -> str:
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

def get_inspiring_deity(nakshatra_lord: str) -> str:
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

def get_lucky_direction(nakshatra_lord: str) -> str:
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

def get_lucky_letter(nakshatra_lord: str) -> str:
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

def get_favourable_metal(nakshatra_lord: str) -> str:
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

def get_ascendant_lord(sign: str) -> str:
    """
    Returns ascendant lord based on zodiac sign.
    
    Args:
        sign (str): Zodiac sign name
        
    Returns:
        str: Planet lord of the sign
    """
    return ZODIAC_SIGNS.get(sign, "Unknown")

def get_moon_sign(planets: dict) -> str:
    """
    Returns Moon sign from planet data.
    
    Args:
        planets (dict): Dictionary containing planet positions
        
    Returns:
        str: Moon sign name
    """
    if 'Moon' in planets:
        return planets['Moon'].get('sign', 'Unknown')
    return 'Unknown'

def get_charakarakas(planets: dict) -> dict:
    """
    Returns atma_karaka and amatya_karaka by sorting planetary degrees.
    
    Args:
        planets (dict): Dictionary containing planet positions
        
    Returns:
        dict: Dictionary with atma_karaka and amatya_karaka
    """
    # Filter planets that have degrees
    planet_degrees = {}
    for planet, data in planets.items():
        if isinstance(data, dict) and 'deg' in data:
            planet_degrees[planet] = data['deg']
    
    # Sort planets by degree (descending order for karakas)
    sorted_planets = sorted(planet_degrees.items(), key=lambda x: x[1], reverse=True)
    
    if len(sorted_planets) >= 2:
        atma_karaka = sorted_planets[0][0]  # Highest degree
        amatya_karaka = sorted_planets[1][0]  # Second highest degree
    else:
        atma_karaka = "Mercury"
        amatya_karaka = "Sun"
    
    return {
        'atma_karaka': atma_karaka,
        'amatya_karaka': amatya_karaka
    }

def calculate_nakshatra_details(moon_position: float) -> dict:
    """
    Calculate nakshatra details from moon position.
    
    Args:
        moon_position (float): Moon's position in degrees
        
    Returns:
        dict: Nakshatra details
    """
    nakshatra_number = int(moon_position / 13.3333) + 1
    if nakshatra_number > 27:
        nakshatra_number = 27
    
    charan = int((moon_position % 13.3333) / 3.3333) + 1
    if charan > 4:
        charan = 4
    
    nakshatra_lord = NAKSHATRA_LORDS.get(nakshatra_number, "Unknown")
    
    return {
        'nakshatra_number': nakshatra_number,
        'charan': charan,
        'nakshatra_lord': nakshatra_lord
    }

def extract_basic_details(kundli: dict) -> dict:
    """
    Extracts Basic Details from Kundli data.
    
    Args:
        kundli (dict): Complete Kundli data
        
    Returns:
        dict: Basic Details dictionary
    """
    try:
        # Get input data
        input_data = kundli.get('input', {})
        date_str = input_data.get('date', '')
        time_str = input_data.get('time', '')
        lat = input_data.get('lat', 0)
        lon = input_data.get('lon', 0)
        tz = input_data.get('tz', 5.5)
        
        # Parse date and time
        if date_str and time_str:
            dob = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            time_formatted = dob.strftime("%I:%M:%S %p")
            date_formatted = dob.strftime("%d %b %Y")
        else:
            time_formatted = time_str
            date_formatted = date_str
        
        # Format timezone
        tz_str = f"+{int(tz):02d}:{int((tz % 1) * 60):02d}" if tz >= 0 else f"-{int(abs(tz)):02d}:{int((abs(tz) % 1) * 60):02d}"
        
        # Get planet data
        planets = kundli.get('planets', {})
        
        # Get Moon sign
        moon_sign = get_moon_sign(planets)
        
        # Get Sun sign
        sun_sign = planets.get('Sun', {}).get('sign', 'Unknown')
        
        # Get Ascendant from lagna data
        lagna = kundli.get('lagna', {})
        ascendant = lagna.get('sign', 'Unknown')
        
        # Calculate Ayanamsa (simplified)
        ayanamsa = 23.47  # Approximate value for Lahiri Ayanamsa
        
        # Format coordinates
        lat_deg = int(lat)
        lat_min = int((lat % 1) * 60)
        lon_deg = int(lon)
        lon_min = int((lon % 1) * 60)
        
        return {
            'name': 'Not specified',
            'gender': 'Not specified',
            'date_of_birth': date_formatted,
            'time_of_birth': f"{time_formatted} Standard Time",
            'timezone': f"{tz_str} East of Greenwich" if tz >= 0 else f"{tz_str} West of Greenwich",
            'moon_sign': moon_sign,
            'ascendant': ascendant,
            'sun_sign_western': sun_sign,
            'place_of_birth': 'Not specified',
            'country': 'India',
            'longitude_latitude': f"{lon_deg}.{lon_min:02d} East, {lat_deg}.{lat_min:02d} North",
            'ayanamsa': f"Chitra Paksha = {int(ayanamsa)}Deg. {int((ayanamsa % 1) * 60)}Min. {int(((ayanamsa % 1) * 60 % 1) * 60)}Sec."
        }
    except Exception as e:
        print(f"Error extracting basic details: {e}")
        return {
            'name': 'Not specified',
            'gender': 'Not specified',
            'date_of_birth': date_str,
            'time_of_birth': time_str,
            'timezone': f"+{tz}" if tz >= 0 else f"{tz}",
            'moon_sign': 'Unknown',
            'ascendant': 'Unknown',
            'sun_sign_western': 'Unknown',
            'place_of_birth': 'Not specified',
            'country': 'India',
            'longitude_latitude': f"{lon}, {lat}",
            'ayanamsa': 'Not calculated'
        }

def extract_astrological_details(kundli: dict) -> dict:
    """
    Extracts Astrological Details from Kundli data.
    
    Args:
        kundli (dict): Complete Kundli data
        
    Returns:
        dict: Astrological Details dictionary
    """
    try:
        # Get planet data
        planets = kundli.get('planets', {})
        
        # Get Sun sign and lord
        sun_sign = planets.get('Sun', {}).get('sign', 'Unknown')
        sign_lord = get_ascendant_lord(sun_sign)
        
        # Get Ascendant and its lord
        lagna = kundli.get('lagna', {})
        ascendant = lagna.get('sign', 'Unknown')
        ascendant_lord = get_ascendant_lord(ascendant)
        
        # Calculate charakarakas
        charakarakas = get_charakarakas(planets)
        
        # Calculate nakshatra details from Moon position
        moon_data = planets.get('Moon', {})
        moon_deg = moon_data.get('deg', 0)
        
        # Calculate Moon's absolute position
        moon_sign_num = 0
        if 'Moon' in planets:
            # Estimate moon position from sign
            moon_sign = planets['Moon'].get('sign', '')
            for i, sign in enumerate(ZODIAC_SIGNS.keys()):
                if sign == moon_sign:
                    moon_sign_num = i
                    break
            moon_absolute_pos = moon_sign_num * 30 + moon_deg
        else:
            moon_absolute_pos = 0
        
        nakshatra_details = calculate_nakshatra_details(moon_absolute_pos)
        
        # Name alphabet and nakshatra charan alphabet (simplified)
        name_alphabet = "Ma, Ta | म, ट"
        nakshatra_charan_alphabet = "मू (Moo)"
        
        # Paya (element) - simplified mapping
        paya = "Iron"
        
        return {
            'sign_lord': sign_lord,
            'nakshatra_lord': nakshatra_details['nakshatra_lord'],
            'charan': nakshatra_details['charan'],
            'name_alphabet': name_alphabet,
            'nakshatra_charan_alphabet': nakshatra_charan_alphabet,
            'paya': paya,
            'ascendant_lord': ascendant_lord,
            'atma_karaka': charakarakas['atma_karaka'],
            'amatya_karaka': charakarakas['amatya_karaka'],
            'dasha_system': "Vimshottari, Years = 365.25 Days"
        }
    except Exception as e:
        print(f"Error extracting astrological details: {e}")
        return {
            'sign_lord': 'Unknown',
            'nakshatra_lord': 'Unknown',
            'charan': 0,
            'name_alphabet': 'Not calculated',
            'nakshatra_charan_alphabet': 'Not calculated',
            'paya': 'Not calculated',
            'ascendant_lord': 'Unknown',
            'atma_karaka': 'Unknown',
            'amatya_karaka': 'Unknown',
            'dasha_system': "Vimshottari, Years = 365.25 Days"
        }

def calculate_comprehensive_details_from_kundli(kundli: dict) -> dict:
    """
    Calculate comprehensive details using the existing Kundli data.
    
    Args:
        kundli (dict): Complete Kundli data from app.py
        
    Returns:
        dict: Comprehensive details with Basic and Astrological sections
    """
    try:
        # Extract basic details
        basic_details = extract_basic_details(kundli)
        
        # Extract astrological details
        astrological_details = extract_astrological_details(kundli)
        
        # Calculate panchang details using the new function
        panchang_details = calculate_panchang_details_from_kundli(kundli)
        
        # Calculate lucky points based on nakshatra lord
        nakshatra_lord = astrological_details.get('nakshatra_lord', 'Moon')
        lucky_points = {
            'favourable_days': get_favourable_days(nakshatra_lord),
            'favourable_color': get_favourable_color(nakshatra_lord),
            'lucky_number': get_lucky_number(nakshatra_lord),
            'inspiring_deity': get_inspiring_deity(nakshatra_lord),
            'lucky_direction': get_lucky_direction(nakshatra_lord),
            'lucky_letter': get_lucky_letter(nakshatra_lord),
            'favourable_metal': get_favourable_metal(nakshatra_lord)
        }
        
        return {
            'basic_details': basic_details,
            'astrological_details': astrological_details,
            'panchang_details': panchang_details,
            'lucky_points': lucky_points
        }
    except Exception as e:
        print(f"Error calculating comprehensive details: {e}")
        return {
            'basic_details': extract_basic_details(kundli),
            'astrological_details': extract_astrological_details(kundli),
            'panchang_details': calculate_panchang_details_from_kundli(kundli),
            'lucky_points': {
                'favourable_days': 'Not calculated',
                'favourable_color': 'Not calculated',
                'lucky_number': 'Not calculated',
                'inspiring_deity': 'Not calculated',
                'lucky_direction': 'Not calculated',
                'lucky_letter': 'Not calculated',
                'favourable_metal': 'Not calculated'
            }
        } 

def calculate_panchang_details_from_kundli(kundli: dict) -> dict:
    """
    Calculate Panchang Details from existing Kundli data.
    
    Args:
        kundli (dict): Complete Kundli data
        
    Returns:
        dict: Panchang Details dictionary
    """
    try:
        # Get input data
        input_data = kundli.get('input', {})
        date_str = input_data.get('date', '')
        time_str = input_data.get('time', '')
        
        # Parse date and time
        if date_str and time_str:
            dob = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            weekday = dob.strftime("%A")
            local_mean_time = dob.strftime("%H:%M:%S")
        else:
            weekday = "Unknown"
            local_mean_time = time_str
        
        # Get planet data
        planets = kundli.get('planets', {})
        
        # Calculate Moon's absolute position for nakshatra
        moon_data = planets.get('Moon', {})
        moon_deg = moon_data.get('deg', 0)
        
        # Calculate Moon's sign number
        moon_sign_num = 0
        if 'Moon' in planets:
            moon_sign = planets['Moon'].get('sign', '')
            for i, sign in enumerate(ZODIAC_SIGNS.keys()):
                if sign == moon_sign:
                    moon_sign_num = i
                    break
        
        # Calculate absolute moon position
        moon_absolute_pos = moon_sign_num * 30 + moon_deg
        
        # Calculate nakshatra
        nakshatra_number = int(moon_absolute_pos / 13.3333) + 1
        if nakshatra_number > 27:
            nakshatra_number = 27
        birth_star_nakshatra = NAKSHATRA_NAMES[nakshatra_number - 1]
        
        # Calculate Sun's absolute position
        sun_data = planets.get('Sun', {})
        sun_deg = sun_data.get('deg', 0)
        
        # Calculate Sun's sign number
        sun_sign_num = 0
        if 'Sun' in planets:
            sun_sign = planets['Sun'].get('sign', '')
            for i, sign in enumerate(ZODIAC_SIGNS.keys()):
                if sign == sun_sign:
                    sun_sign_num = i
                    break
        
        # Calculate absolute sun position
        sun_absolute_pos = sun_sign_num * 30 + sun_deg
        
        # Calculate lunar phase (tithi)
        lunar_phase = (moon_absolute_pos - sun_absolute_pos) % 360
        tithi_number = int(lunar_phase / 12) + 1
        if tithi_number > 30:
            tithi_number = 30
        tithi_lunar_day = TITHI_NAMES[tithi_number - 1]
        
        # Calculate karan
        karana_number = int(lunar_phase / 6) + 1
        if karana_number > 11:
            karana_number = 11
        karan = KARANA_NAMES[karana_number - 1] if karana_number <= len(KARANA_NAMES) else f"Karana {karana_number}"
        
        # Calculate nithya yoga
        yoga_number = int((sun_absolute_pos + moon_absolute_pos) / 13.3333) + 1
        if yoga_number > 27:
            yoga_number = 27
        nithya_yoga = YOGA_NAMES[yoga_number - 1] if yoga_number <= len(YOGA_NAMES) else f"Yoga {yoga_number}"
        
        # Calculate sunrise and sunset (simplified based on date)
        # For now, use approximate times based on season
        month = dob.month if date_str else 1
        if month in [12, 1, 2]:  # Winter
            sunrise = "07:00"
            sunset = "17:30"
        elif month in [3, 4, 5]:  # Spring
            sunrise = "06:00"
            sunset = "18:00"
        elif month in [6, 7, 8]:  # Summer
            sunrise = "05:30"
            sunset = "19:00"
        else:  # Autumn
            sunrise = "06:30"
            sunset = "17:30"
        
        return {
            'sunrise': sunrise,
            'sunset': sunset,
            'local_mean_time': local_mean_time,
            'weekday': weekday,
            'birth_star_nakshatra': birth_star_nakshatra,
            'tithi_lunar_day': tithi_lunar_day,
            'karan': karan,
            'nithya_yoga': nithya_yoga
        }
    except Exception as e:
        print(f"Error calculating panchang details: {e}")
        return {
            'sunrise': '06:00',
            'sunset': '18:00',
            'local_mean_time': time_str,
            'weekday': 'Monday',
            'birth_star_nakshatra': 'Rohini',
            'tithi_lunar_day': 'Pratipada',
            'karan': 'Bava',
            'nithya_yoga': 'Vishkambha'
        } 