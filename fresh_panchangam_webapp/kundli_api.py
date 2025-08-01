#!/usr/bin/env python3
"""
Kundli API - Comprehensive Vedic Astrology API
Provides endpoints for Kundli generation, analysis, and detailed astrological calculations.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import swisseph as swe
import pytz
from functools import wraps
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint for Kundli API
kundli_api = Blueprint('kundli_api', __name__)

# Constants
RASHI_NAMES = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
    "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrischika (Scorpio)",
    "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER, 'Venus': swe.VENUS, 'Saturn': swe.SATURN,
    'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE, 'Pluto': swe.PLUTO,
    'Rahu (Mean)': swe.MEAN_NODE
}

def validate_input(f):
    """Decorator to validate API input parameters"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400
            
            required_fields = ['date', 'time', 'lat', 'lon', 'tz']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Validate date format
            try:
                datetime.strptime(f"{data['date']} {data['time']}", "%Y-%m-%d %H:%M")
            except ValueError:
                return jsonify({'error': 'Invalid date/time format. Use YYYY-MM-DD HH:MM'}), 400
            
            # Validate coordinates
            try:
                lat = float(data['lat'])
                lon = float(data['lon'])
                tz = float(data['tz'])
                
                if not (-90 <= lat <= 90):
                    return jsonify({'error': 'Latitude must be between -90 and 90'}), 400
                if not (-180 <= lon <= 180):
                    return jsonify({'error': 'Longitude must be between -180 and 180'}), 400
                if not (-12 <= tz <= 14):
                    return jsonify({'error': 'Timezone must be between -12 and 14'}), 400
                    
            except ValueError:
                return jsonify({'error': 'Invalid coordinates or timezone format'}), 400
                
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Input validation error: {e}")
            return jsonify({'error': 'Invalid input data'}), 400
    
    return decorated_function

def get_navamsha_sign(sign, deg):
    """Calculate Navamsha sign from Rashi and degree"""
    segment = int(deg / 3.3333)
    return ((sign - 1) * 9 + segment) % 12 + 1

def calculate_planet_positions(dob, lat, lon, tz):
    """Calculate positions of all planets"""
    jd_ut = swe.julday(dob.year, dob.month, dob.day, dob.hour + dob.minute/60 - tz)
    
    # Set ephemeris path and sidereal mode
    swe.set_ephe_path('../jyotisha/panchaanga/temporal/data')
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    planet_positions = {}
    
    # Calculate positions for all planets
    for planet, code in PLANETS.items():
        try:
            pos = swe.calc_ut(jd_ut, code, flags=swe.FLG_SIDEREAL)[0][0]
            sign = int(pos / 30)
            deg = pos % 30
            nav_sign = get_navamsha_sign(sign + 1, deg)
            
            planet_positions[planet] = {
                'longitude': pos,
                'degree': deg,
                'sign': RASHI_NAMES[sign],
                'sign_number': sign + 1,
                'navamsha_sign': RASHI_NAMES[nav_sign - 1],
                'navamsha_sign_number': nav_sign
            }
        except Exception as e:
            logger.error(f"Error calculating {planet}: {e}")
            planet_positions[planet] = {'error': f'Failed to calculate {planet}'}
    
    # Calculate Ketu (opposite to Rahu)
    try:
        rahu_pos = swe.calc_ut(jd_ut, swe.MEAN_NODE, flags=swe.FLG_SIDEREAL)[0][0]
        ketu_pos = (rahu_pos + 180) % 360
        ketu_sign = int(ketu_pos / 30)
        ketu_deg = ketu_pos % 30
        ketu_nav = get_navamsha_sign(ketu_sign + 1, ketu_deg)
        
        planet_positions['Ketu (Mean)'] = {
            'longitude': ketu_pos,
            'degree': ketu_deg,
            'sign': RASHI_NAMES[ketu_sign],
            'sign_number': ketu_sign + 1,
            'navamsha_sign': RASHI_NAMES[ketu_nav - 1],
            'navamsha_sign_number': ketu_nav
        }
    except Exception as e:
        logger.error(f"Error calculating Ketu: {e}")
        planet_positions['Ketu (Mean)'] = {'error': 'Failed to calculate Ketu'}
    
    return planet_positions, jd_ut

def calculate_lagna_and_houses(jd_ut, lat, lon):
    """Calculate Lagna (Ascendant) and house positions"""
    try:
        cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'A', flags=swe.FLG_SIDEREAL)
        lagna_full_deg = ascmc[0]
        lagna_deg = lagna_full_deg % 30
        lagna_sign_index = int(lagna_full_deg / 30)
        
        lagna = {
            'longitude': lagna_full_deg,
            'degree': lagna_deg,
            'sign': RASHI_NAMES[lagna_sign_index],
            'sign_number': lagna_sign_index + 1
        }
        
        # Calculate house positions
        houses = []
        for i, cusp in enumerate(cusps[:12]):
            house_sign = int(cusp / 30)
            house_deg = cusp % 30
            houses.append({
                'house_number': i + 1,
                'longitude': cusp,
                'degree': house_deg,
                'sign': RASHI_NAMES[house_sign],
                'sign_number': house_sign + 1
            })
        
        return lagna, houses
        
    except Exception as e:
        logger.error(f"Error calculating Lagna and houses: {e}")
        return None, []

def calculate_relative_houses(planet_positions, lagna):
    """Calculate relative house positions for planets"""
    if not lagna:
        return planet_positions
    
    lagna_longitude = lagna['longitude']
    
    for planet, data in planet_positions.items():
        if 'longitude' in data and 'error' not in data:
            planet_longitude = data['longitude']
            # Calculate relative house (1-12)
            relative_house = int((planet_longitude - lagna_longitude) / 30) + 1
            if relative_house <= 0:
                relative_house += 12
            data['house'] = relative_house
    
    return planet_positions

@kundli_api.route('/api/kundli/basic', methods=['POST'])
@validate_input
def generate_basic_kundli():
    """
    Generate basic Kundli with planet positions and Lagna
    
    Request Body:
    {
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "lat": float,
        "lon": float,
        "tz": float,
        "name": "string (optional)",
        "gender": "string (optional)"
    }
    
    Returns:
    {
        "input": {...},
        "planets": {...},
        "lagna": {...},
        "houses": [...]
    }
    """
    try:
        data = request.get_json()
        date_str = data['date']
        time_str = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])
        tz = float(data['tz'])
        name = data.get('name', '')
        gender = data.get('gender', '')
        
        dob = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        
        # Calculate planet positions
        planet_positions, jd_ut = calculate_planet_positions(dob, lat, lon, tz)
        
        # Calculate Lagna and houses
        lagna, houses = calculate_lagna_and_houses(jd_ut, lat, lon)
        
        # Calculate relative houses
        planet_positions = calculate_relative_houses(planet_positions, lagna)
        
        return jsonify({
            'status': 'success',
            'input': {
                'date': date_str,
                'time': time_str,
                'lat': lat,
                'lon': lon,
                'tz': tz,
                'name': name,
                'gender': gender
            },
            'planets': planet_positions,
            'lagna': lagna,
            'houses': houses,
            'julian_day': jd_ut
        })
        
    except Exception as e:
        logger.error(f"Error in basic kundli generation: {e}")
        return jsonify({'error': f'Failed to generate kundli: {str(e)}'}), 500

@kundli_api.route('/api/kundli/comprehensive', methods=['POST'])
@validate_input
def generate_comprehensive_kundli():
    """
    Generate comprehensive Kundli with all astrological details
    
    Request Body:
    {
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "lat": float,
        "lon": float,
        "tz": float,
        "name": "string (optional)",
        "gender": "string (optional)"
    }
    
    Returns:
    {
        "input": {...},
        "planets": {...},
        "lagna": {...},
        "houses": [...],
        "yogas": [...],
        "doshas": [...],
        "comprehensive_details": {...}
    }
    """
    try:
        data = request.get_json()
        date_str = data['date']
        time_str = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])
        tz = float(data['tz'])
        name = data.get('name', '')
        gender = data.get('gender', '')
        
        dob = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        
        # Calculate basic kundli
        planet_positions, jd_ut = calculate_planet_positions(dob, lat, lon, tz)
        lagna, houses = calculate_lagna_and_houses(jd_ut, lat, lon)
        planet_positions = calculate_relative_houses(planet_positions, lagna)
        
        # Calculate Tithi and Nakshatra
        sun_pos = swe.calc_ut(jd_ut, swe.SUN, flags=swe.FLG_SIDEREAL)[0][0]
        moon_pos = swe.calc_ut(jd_ut, swe.MOON, flags=swe.FLG_SIDEREAL)[0][0]
        
        lunar_phase = (moon_pos - sun_pos) % 360
        tithi_number = int(lunar_phase / 12) + 1
        nakshatra_number = int(moon_pos / 13.3333) + 1
        
        # Detect yogas and doshas
        try:
            from yoga_rules import detect_all_yogas
            from dosha_rules import detect_all_doshas
            
            time_info = {
                'tithi': tithi_number,
                'nakshatra': nakshatra_number,
                'lunar_phase': lunar_phase,
                'sun_position': sun_pos,
                'moon_position': moon_pos
            }
            
            kundli_data = {
                'planets': planet_positions,
                'lagna': lagna,
                'houses': houses,
                'input': data
            }
            
            detected_yogas = detect_all_yogas(planet_positions, houses, lagna, time_info)
            detected_doshas = detect_all_doshas(kundli_data)
            
        except Exception as e:
            logger.error(f"Error detecting yogas/doshas: {e}")
            detected_yogas = []
            detected_doshas = []
        
        # Calculate comprehensive details
        try:
            from kundli_details import calculate_comprehensive_kundli_details
            comprehensive_details = calculate_comprehensive_kundli_details(
                date_str, time_str, lat, lon, tz, name, gender
            )
        except Exception as e:
            logger.error(f"Error calculating comprehensive details: {e}")
            comprehensive_details = {
                'basic_details': {},
                'astrological_details': {},
                'panchang_details': {},
                'lucky_points': {}
            }
        
        return jsonify({
            'status': 'success',
            'input': {
                'date': date_str,
                'time': time_str,
                'lat': lat,
                'lon': lon,
                'tz': tz,
                'name': name,
                'gender': gender
            },
            'planets': planet_positions,
            'lagna': lagna,
            'houses': houses,
            'tithi': tithi_number,
            'nakshatra': nakshatra_number,
            'yogas': detected_yogas,
            'doshas': detected_doshas,
            'comprehensive_details': comprehensive_details,
            'julian_day': jd_ut
        })
        
    except Exception as e:
        logger.error(f"Error in comprehensive kundli generation: {e}")
        return jsonify({'error': f'Failed to generate comprehensive kundli: {str(e)}'}), 500

@kundli_api.route('/api/kundli/planets', methods=['POST'])
@validate_input
def get_planet_positions():
    """
    Get only planet positions for a given date/time/location
    
    Request Body:
    {
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "lat": float,
        "lon": float,
        "tz": float
    }
    
    Returns:
    {
        "planets": {...},
        "julian_day": float
    }
    """
    try:
        data = request.get_json()
        date_str = data['date']
        time_str = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])
        tz = float(data['tz'])
        
        dob = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        planet_positions, jd_ut = calculate_planet_positions(dob, lat, lon, tz)
        
        return jsonify({
            'status': 'success',
            'planets': planet_positions,
            'julian_day': jd_ut
        })
        
    except Exception as e:
        logger.error(f"Error getting planet positions: {e}")
        return jsonify({'error': f'Failed to get planet positions: {str(e)}'}), 500

@kundli_api.route('/api/kundli/lagna', methods=['POST'])
@validate_input
def get_lagna():
    """
    Get Lagna (Ascendant) and house positions
    
    Request Body:
    {
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "lat": float,
        "lon": float,
        "tz": float
    }
    
    Returns:
    {
        "lagna": {...},
        "houses": [...],
        "julian_day": float
    }
    """
    try:
        data = request.get_json()
        date_str = data['date']
        time_str = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])
        tz = float(data['tz'])
        
        dob = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        jd_ut = swe.julday(dob.year, dob.month, dob.day, dob.hour + dob.minute/60 - tz)
        
        lagna, houses = calculate_lagna_and_houses(jd_ut, lat, lon)
        
        return jsonify({
            'status': 'success',
            'lagna': lagna,
            'houses': houses,
            'julian_day': jd_ut
        })
        
    except Exception as e:
        logger.error(f"Error getting Lagna: {e}")
        return jsonify({'error': f'Failed to get Lagna: {str(e)}'}), 500

@kundli_api.route('/api/kundli/docs', methods=['GET'])
def api_documentation():
    """
    Get API documentation
    """
    return jsonify({
        'api_name': 'Kundli API',
        'version': '1.0.0',
        'description': 'Comprehensive Vedic Astrology API for Kundli generation and analysis',
        'endpoints': {
            '/api/kundli/basic': {
                'method': 'POST',
                'description': 'Generate basic Kundli with planet positions and Lagna',
                'required_fields': ['date', 'time', 'lat', 'lon', 'tz'],
                'optional_fields': ['name', 'gender']
            },
            '/api/kundli/comprehensive': {
                'method': 'POST',
                'description': 'Generate comprehensive Kundli with all astrological details',
                'required_fields': ['date', 'time', 'lat', 'lon', 'tz'],
                'optional_fields': ['name', 'gender']
            },
            '/api/kundli/planets': {
                'method': 'POST',
                'description': 'Get only planet positions',
                'required_fields': ['date', 'time', 'lat', 'lon', 'tz']
            },
            '/api/kundli/lagna': {
                'method': 'POST',
                'description': 'Get Lagna (Ascendant) and house positions',
                'required_fields': ['date', 'time', 'lat', 'lon', 'tz']
            },
            '/api/kundli/docs': {
                'method': 'GET',
                'description': 'Get API documentation'
            }
        },
        'date_format': 'YYYY-MM-DD',
        'time_format': 'HH:MM (24-hour)',
        'coordinates': 'Decimal degrees',
        'timezone': 'Hours offset from UTC (e.g., 5.5 for IST)'
    }) 