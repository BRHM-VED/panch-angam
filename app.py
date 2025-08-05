#!/usr/bin/env python3
"""
Clean Kundli and Dosha Detection API
Simple Flask application for astrological calculations
"""

from flask import Flask, request, jsonify
import swisseph as swe
from datetime import datetime
import pytz
import os

app = Flask(__name__)

# Initialize Swiss Ephemeris
swe.set_ephe_path()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "message": "Kundli and Dosha Detection API",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/kundli', methods=['POST'])
def generate_kundli():
    """Generate basic kundli details"""
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['date', 'time', 'lat', 'lon', 'tz']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Parse date and time
        date_str = data['date']
        time_str = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])
        tz = float(data['tz'])
        
        # Convert to datetime
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        
        # Calculate Julian Day
        jd = swe.date_conversion(dt.year, dt.month, dt.day, dt.hour + dt.minute/60 - tz)
        
        # Calculate houses
        houses = swe.houses(jd, lat, lon, b'P')
        lagna_pos = houses[0][0]
        lagna_sign = int(lagna_pos / 30) + 1
        
        # Calculate planet positions
        planets = {}
        planet_codes = {
            'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 
            'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER, 
            'Venus': swe.VENUS, 'Saturn': swe.SATURN,
            'Rahu': swe.MEAN_NODE
        }
        
        sign_names = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        for planet_name, planet_code in planet_codes.items():
            try:
                result = swe.calc_ut(jd, planet_code, flags=swe.FLG_SIDEREAL)
                planet_pos = result[0][0]
                sign_num = int(planet_pos / 30) + 1
                house_num = ((sign_num - lagna_sign) % 12) + 1
                
                planets[planet_name] = {
                    'position': planet_pos,
                    'sign': sign_names[sign_num - 1],
                    'house': house_num,
                    'degree': planet_pos % 30
                }
            except Exception as e:
                planets[planet_name] = {'error': str(e)}
        
        # Calculate Ketu (opposite to Rahu)
        if 'Rahu' in planets and 'position' in planets['Rahu']:
            ketu_pos = (planets['Rahu']['position'] + 180) % 360
            ketu_sign = int(ketu_pos / 30) + 1
            ketu_house = ((ketu_sign - lagna_sign) % 12) + 1
            planets['Ketu'] = {
                'position': ketu_pos,
                'sign': sign_names[ketu_sign - 1],
                'house': ketu_house,
                'degree': ketu_pos % 30
            }
        
        return jsonify({
            "input": data,
            "julian_day": jd,
            "lagna": {
                "position": lagna_pos,
                "sign": sign_names[lagna_sign - 1],
                "house": 1
            },
            "planets": planets
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dosha-detection', methods=['POST'])
def detect_doshas():
    """Detect various doshas based on kundli"""
    try:
        data = request.get_json()
        
        # First generate kundli
        kundli_response = generate_kundli()
        if kundli_response.status_code != 200:
            return kundli_response
        
        kundli_data = kundli_response.get_json()
        planets = kundli_data['planets']
        
        doshas = []
        
        # Sade Sati Detection
        if 'Saturn' in planets and 'Moon' in planets:
            saturn_house = planets['Saturn']['house']
            moon_house = planets['Moon']['house']
            
            # Check if Saturn is in 12th, 1st, or 2nd house from Moon
            house_diff = (saturn_house - moon_house) % 12
            if house_diff in [0, 1, 11]:  # 12th, 1st, or 2nd house
                doshas.append({
                    "name": "Sade Sati",
                    "description": "Saturn in 12th, 1st, or 2nd house from Moon",
                    "effects": "7.5 years of challenges, health issues, career obstacles",
                    "remedies": "Wear blue sapphire, perform Saturn puja, donate black items",
                    "severity": "Moderate",
                    "type": "Major Dosha"
                })
        
        # Pitra Dosha Detection
        if 'Rahu' in planets and planets['Rahu']['house'] == 9:
            doshas.append({
                "name": "Pitra Dosha",
                "description": "Rahu in 9th house (father's house)",
                "effects": "Ancestral curses, father-related issues, property disputes",
                "remedies": "Perform Pitra puja, donate to Brahmins, visit holy places",
                "severity": "Moderate",
                "type": "Ancestral Dosha"
            })
        
        # Kaal Sarp Dosha Detection
        if 'Rahu' in planets and 'Ketu' in planets:
            rahu_pos = planets['Rahu']['position']
            ketu_pos = planets['Ketu']['position']
            
            # Check if all planets are between Rahu and Ketu
            all_planets_between = True
            for planet_name, planet_data in planets.items():
                if planet_name not in ['Rahu', 'Ketu'] and 'position' in planet_data:
                    planet_pos = planet_data['position']
                    # Check if planet is between Rahu and Ketu
                    if not (min(rahu_pos, ketu_pos) <= planet_pos <= max(rahu_pos, ketu_pos)):
                        all_planets_between = False
                        break
            
            if all_planets_between:
                doshas.append({
                    "name": "Kaal Sarp Dosha",
                    "description": "All planets between Rahu and Ketu",
                    "effects": "Life obstacles, delays in success, health issues",
                    "remedies": "Perform Kaal Sarp puja, wear gemstones, visit temples",
                    "severity": "High",
                    "type": "Major Dosha"
                })
        
        # Wealth Dosha Detection
        malefic_planets = ['Mars', 'Saturn', 'Rahu', 'Ketu']
        for planet_name in malefic_planets:
            if planet_name in planets and planets[planet_name]['house'] in [2, 11]:
                doshas.append({
                    "name": "Wealth Dosha",
                    "description": f"{planet_name} in {planets[planet_name]['house']}nd house",
                    "effects": "Financial difficulties, wealth obstacles",
                    "remedies": "Perform Lakshmi puja, donate to charity, wear yellow sapphire",
                    "severity": "Moderate",
                    "type": "Wealth Dosha"
                })
                break
        
        return jsonify({
            "input": data,
            "kundli": kundli_data,
            "doshas": doshas
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Kundli and Dosha Detection API",
        "endpoints": [
            "/health",
            "/kundli",
            "/dosha-detection"
        ],
        "usage": {
            "kundli": "POST /kundli with date, time, lat, lon, tz",
            "dosha": "POST /dosha-detection with same parameters"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
