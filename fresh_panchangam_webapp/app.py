import os
import subprocess
import json
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, timezone
import pytz
from werkzeug.utils import secure_filename
import sys
from flask_cors import CORS
import swisseph as swe

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from yoga_rules import detect_all_yogas
    from yoga_utils import get_planet_strength, is_exalted, is_debilitated, get_sign_lord
    from dosha_rules import detect_all_doshas
    from kundli_details import calculate_comprehensive_kundli_details
except ImportError:
    # Fallback for deployment environment
    def detect_all_yogas(planets, bhavas, lagna):
        return []
    
    def detect_all_doshas(kundli):
        return []
    
    def calculate_comprehensive_kundli_details(date_str, time_str, lat, lon, tz, name="", gender=""):
        return {
            'basic_details': {},
            'astrological_details': {},
            'panchang_details': {},
            'lucky_points': {}
        }
    
    def get_planet_strength(planet, sign_number):
        return "Neutral"
    
    def is_exalted(planet, sign_number):
        return False
    
    def is_debilitated(planet, sign_number):
        return False
    
    def get_sign_lord(sign_number):
        return "Unknown"

app = Flask(__name__)
CORS(app)

TITHI_NAMES = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami",
    "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada (Krishna)", "Dvitiya (Krishna)", "Tritiya (Krishna)", "Chaturthi (Krishna)", "Panchami (Krishna)",
    "Shashthi (Krishna)", "Saptami (Krishna)", "Ashtami (Krishna)", "Navami (Krishna)", "Dashami (Krishna)",
    "Ekadashi (Krishna)", "Dwadashi (Krishna)", "Trayodashi (Krishna)", "Chaturdashi (Krishna)", "Amavasya"
]
KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
] + [None] * 49
YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
]
NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]
RASHI_NAMES = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)", "Simha (Leo)", "Kanya (Virgo)",
    "Tula (Libra)", "Vrischika (Scorpio)", "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

def jd_to_time(jd):
    # Julian day 2451545.0 is 2000-01-01 12:00:00 UTC
    dt_utc = datetime(2000, 1, 1, 12, tzinfo=timezone.utc) + timedelta(days=jd - 2451545.0)
    dt_ist = dt_utc.astimezone(pytz.timezone("Asia/Kolkata"))
    return dt_ist.strftime("%I:%M %p")

def extract_summary(data):
    sunrise = jd_to_time(data["jd_sunrise"])
    sunset = jd_to_time(data["jd_sunset"])
    moonrise = jd_to_time(data["graha_rise_jd"]["moon"])
    moonset = jd_to_time(data["graha_set_jd"]["moon"])
    tithi_strs = []
    for idx, t in enumerate(data["sunrise_day_angas"]["tithis_with_ends"]):
        name = TITHI_NAMES[t["anga"]["index"] - 1]
        end_time = jd_to_time(t["jd_end"]) if "jd_end" in t else "end of day"
        tithi_strs.append(f"{name}" + (f" upto {end_time}" if idx == 0 else ""))
    nakshatra_strs = []
    for idx, n in enumerate(data["sunrise_day_angas"]["nakshatras_with_ends"]):
        name = NAKSHATRA_NAMES[n["anga"]["index"] - 1]
        end_time = jd_to_time(n["jd_end"]) if "jd_end" in n else "end of day"
        nakshatra_strs.append(f"{name}" + (f" upto {end_time}" if idx == 0 else ""))
    yoga_strs = []
    for idx, y in enumerate(data["sunrise_day_angas"]["yogas_with_ends"]):
        name = YOGA_NAMES[y["anga"]["index"] - 1]
        end_time = jd_to_time(y["jd_end"]) if "jd_end" in y else "end of day"
        yoga_strs.append(f"{name}" + (f" upto {end_time}" if idx == 0 else ""))
    karana_strs = []
    for idx, k in enumerate(data["sunrise_day_angas"]["karanas_with_ends"]):
        name = KARANA_NAMES[k["anga"]["index"] - 1] if KARANA_NAMES[k["anga"]["index"] - 1] else f"Karana #{k['anga']['index']}"
        end_time = jd_to_time(k["jd_end"]) if "jd_end" in k else "end of day"
        karana_strs.append(f"{name}" + (f" upto {end_time}" if "jd_end" in k else ""))
    weekday = datetime(data["date"]["year"], data["date"]["month"], data["date"]["day"]).strftime("%A")
    paksha = "Shukla Paksha" if data["lunar_date"]["index"] <= 15 else "Krishna Paksha"
    moonsign = RASHI_NAMES[data["sunrise_day_angas"]["raashis_with_ends"][0]["anga"]["index"] - 1]
    sunsign = RASHI_NAMES[data["sunrise_day_angas"]["graha_raashis_with_ends"]["sun"][0]["anga"]["index"] - 1]
    summary = {
        "Sunrise": sunrise,
        "Sunset": sunset,
        "Moonrise": moonrise,
        "Moonset": moonset,
        "Tithi": tithi_strs,
        "Nakshatra": nakshatra_strs,
        "Yoga": yoga_strs,
        "Karana": karana_strs,
        "Weekday": weekday,
        "Paksha": paksha,
        "Moonsign": moonsign,
        "Sunsign": sunsign
    }
    return summary

@app.route('/', methods=['GET'])
def index():
    return render_template('index_fresh.html')

@app.route('/get_panchang', methods=['POST'])
def get_panchang():
    data = request.json
    date_str = data.get('date')
    lat = data.get('lat')
    lon = data.get('lon')
    location = data.get('location', 'Unknown')
    year, month, day = map(int, date_str.split('-'))
    tz = 'Asia/Kolkata'
    args = [
        'python', '-m', 'jyotisha.panchaanga.writer.write_daily_panchaanga_json',
        location, str(lat), str(lon), tz, str(year), str(month), str(day)
    ]
    import os
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    try:
        print("Received date:", date_str, "lat:", lat, "lon:", lon, "tz:", tz)
        print("Subprocess command:", args)
        # Dynamically determine the project root (one level up from this file)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.dirname(BASE_DIR)
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env,
            check=True,
            cwd=PROJECT_ROOT
        )
        print("Raw subprocess output:", repr(result.stdout))
        stdout = result.stdout
        start = stdout.find('{')
        end = stdout.rfind('}')
        if start != -1 and end != -1 and end > start:
            json_str = stdout[start:end+1]
            panchang_json = json.loads(json_str)
        else:
            print("Could not find JSON in subprocess output!")
            print("Raw output:", repr(stdout))
            return jsonify({'error': 'Could not extract JSON from output.'}), 500
        summary = extract_summary(panchang_json)
    except subprocess.CalledProcessError as e:
        print('Subprocess error (stdout):', e.stdout)
        print('Subprocess error (stderr):', e.stderr)
        return jsonify({'error': f'Failed to generate Panchangam: {e}', 'details': e.stderr}), 500
    except Exception as e:
        print('General error:', str(e))
        return jsonify({'error': f'Failed to generate Panchangam: {e}'}), 500
    return jsonify({
        'summary': summary,
        'date_str': date_str,
        'location': location,
        'lat': lat,
        'lon': lon
    })

@app.route('/api', methods=['GET'])
def api_docs():
    return jsonify({
        "endpoints": {
            "/get_panchang": {
                "method": "POST",
                "description": "Get Panchangam data for a given date and location.",
                "body": {
                    "date": "YYYY-MM-DD",
                    "lat": "float",
                    "lon": "float",
                    "location": "string"
                },
                "response": {
                    "summary": "object",
                    "date_str": "string",
                    "location": "string",
                    "lat": "float",
                    "lon": "float"
                }
            }
        }
    })

@app.route('/kundli', methods=['GET'])
def kundli_page():
    return render_template('kundli.html')

@app.route('/kundli_new', methods=['GET'])
def kundli_new_page():
    # This can be removed later, but for now, it points back to the old page too
    return render_template('kundli.html')

@app.route('/api/kundli', methods=['POST'])
def generate_kundli():
    data = request.json
    # Required: date (YYYY-MM-DD), time (HH:MM), lat, lon, tz
    # Optional: name, gender
    try:
        date_str = data['date']
        time_str = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])
        tz = float(data['tz'])
        name = data.get('name', '')  # Optional, default to empty string
        gender = data.get('gender', '')  # Optional, default to empty string
        dob = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except Exception as e:
        return jsonify({'error': f'Invalid input: {e}'}), 400

    rashi_names = [
        "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
        "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrischika (Scorpio)",
        "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
    ]
    planets = {
        'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER, 'Venus': swe.VENUS, 'Saturn': swe.SATURN,
        'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE, 'Pluto': swe.PLUTO,
        'Rahu (Mean)': swe.MEAN_NODE
    }
    def get_navamsha_sign(sign, deg):
        segment = int(deg / 3.3333)
        return ((sign - 1) * 9 + segment) % 12 + 1

    jd_ut = swe.julday(dob.year, dob.month, dob.day, dob.hour + dob.minute/60 - tz)
    
    # Set the ephemeris path correctly for deployment
    swe.set_ephe_path('../jyotisha/panchaanga/temporal/data')
    
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    planet_positions = {}
    for planet, code in planets.items():
        pos = swe.calc_ut(jd_ut, code, flags=swe.FLG_SIDEREAL)[0][0]
        sign = int(pos / 30)
        deg = pos % 30
        nav_sign = get_navamsha_sign(sign + 1, deg)
        planet_positions[planet] = {
            'deg': deg,
            'sign': rashi_names[sign],
            'navamsha_sign': rashi_names[nav_sign - 1]
        }
    # Ketu
    rahu_pos = swe.calc_ut(jd_ut, swe.MEAN_NODE, flags=swe.FLG_SIDEREAL)[0][0]
    ketu_pos = (rahu_pos + 180) % 360
    ketu_sign = int(ketu_pos / 30)
    ketu_deg = ketu_pos % 30
    ketu_nav = get_navamsha_sign(ketu_sign + 1, ketu_deg)
    planet_positions['Ketu (Mean)'] = {
        'deg': ketu_deg,
        'sign': rashi_names[ketu_sign],
        'navamsha_sign': rashi_names[ketu_nav - 1]
    }
    # Import house calculation utilities
    from house_utils import calculate_all_relative_houses, get_relative_house
    
    # Lagna and Bhavas
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'A', flags=swe.FLG_SIDEREAL)
    lagna_full_deg = ascmc[0]  # Full longitude including sign
    lagna_deg = lagna_full_deg % 30
    lagna_sign_index = int(lagna_full_deg / 30)
    lagna = {
        'deg': lagna_deg,
        'sign': rashi_names[lagna_sign_index],
        'sign_number': lagna_sign_index + 1,
        'full_degree': lagna_full_deg
    }

    # Calculate relative houses for all planets based on Lagna
    # This ensures houses are calculated relative to the Lagna sign, not fixed zodiac signs
    for planet in planet_positions:
        if planet in planets:  # Only calculate for planets we have in our dictionary
            planet_pos_deg = swe.calc_ut(jd_ut, planets[planet], flags=swe.FLG_SIDEREAL)[0][0]
            # Calculate house relative to Lagna
            relative_house = get_relative_house(lagna_full_deg, planet_pos_deg)
            planet_positions[planet]['house'] = relative_house
            planet_positions[planet]['longitude'] = planet_pos_deg

    # Also assign house for Ketu based on relative position to Lagna
    ketu_pos_deg = (swe.calc_ut(jd_ut, swe.MEAN_NODE, flags=swe.FLG_SIDEREAL)[0][0] + 180) % 360
    ketu_relative_house = get_relative_house(lagna_full_deg, ketu_pos_deg)
    planet_positions['Ketu (Mean)']['house'] = ketu_relative_house
    planet_positions['Ketu (Mean)']['longitude'] = ketu_pos_deg

    bhavas = []
    for i in range(1, 13): # Ensure 12 bhavas
        # Fixed mapping: House 1=Aries, 2=Taurus, 3=Gemini, etc.
        bhava_sign_index = i - 1  # 0=Aries, 1=Taurus, etc.
        bhavas.append({
            'house': i,
            'sign': rashi_names[bhava_sign_index]
        })

    # Add planet strength information to planet data
    for planet, data in planet_positions.items():
        if 'house' in data:
            # Get the sign number from house (since house = sign in our system)
            sign_number = data['house']
            # Add strength information
            data['strength'] = get_planet_strength(planet, sign_number)
            data['is_exalted'] = is_exalted(planet, sign_number)
            data['is_debilitated'] = is_debilitated(planet, sign_number)
            data['is_own_sign'] = get_sign_lord(sign_number) == planet
    
    # Calculate Tithi and Nakshatra for yoga detection
    # Get Sun and Moon positions for Tithi calculation
    sun_pos = swe.calc_ut(jd_ut, swe.SUN, flags=swe.FLG_SIDEREAL)[0][0]
    moon_pos = swe.calc_ut(jd_ut, swe.MOON, flags=swe.FLG_SIDEREAL)[0][0]
    
    # Calculate Tithi (lunar day)
    lunar_phase = (moon_pos - sun_pos) % 360
    tithi_number = int(lunar_phase / 12) + 1  # 1-30 tithis
    
    # Calculate Nakshatra
    nakshatra_number = int(moon_pos / 13.3333) + 1  # 1-27 nakshatras
    
    # Add time-based information for yoga detection
    time_info = {
        'tithi': tithi_number,
        'nakshatra': nakshatra_number,
        'lunar_phase': lunar_phase,
        'sun_position': sun_pos,
        'moon_position': moon_pos
    }
    
    # Detect yogas in the kundli
    try:
        detected_yogas = detect_all_yogas(planet_positions, bhavas, lagna, time_info)
    except Exception as e:
        print(f"Error detecting yogas: {e}")
        detected_yogas = []
    
    # Prepare kundli data for dosha detection
    kundli_data = {
        'planets': planet_positions,
        'lagna': lagna,
        'bhavas': bhavas,
        'input': {
            'date': date_str,
            'time': time_str,
            'lat': lat,
            'lon': lon,
            'tz': tz
        }
    }
    
    # Detect doshas in the kundli
    try:
        detected_doshas = detect_all_doshas(kundli_data)
    except Exception as e:
        print(f"Error detecting doshas: {e}")
        detected_doshas = []
    
    # Calculate comprehensive kundli details
    try:
        # Use the new astrology_basics module instead of Swiss Ephemeris calculations
        from astrology_basics import calculate_comprehensive_details_from_kundli
        
        # Prepare kundli data for the new module
        kundli_data = {
            'input': {
                'date': date_str,
                'time': time_str,
                'lat': lat,
                'lon': lon,
                'tz': tz
            },
            'planets': planet_positions,
            'lagna': lagna,
            'bhavas': bhavas
        }
        
        comprehensive_details = calculate_comprehensive_details_from_kundli(kundli_data)
        print("Successfully calculated comprehensive details using astrology_basics module")
        
    except Exception as e:
        print(f"Error calculating comprehensive details: {e}")
        # Fallback to basic data
        comprehensive_details = {
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
    
    return jsonify({
        'input': {
            'date': date_str,
            'time': time_str,
            'lat': lat,
            'lon': lon,
            'tz': tz
        },
        'planets': planet_positions,
        'lagna': lagna,
        'bhavas': bhavas,
        'yogas': detected_yogas,
        'doshas': detected_doshas,
        'comprehensive_details': comprehensive_details
    })

@app.route('/get_places', methods=['GET'])
def get_places():
    import os

    places = []
    
    try:
        # Try multiple possible paths for the TSV file
        possible_paths = [
            # Path relative to current directory
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'jyotisha', 'panchaanga', 'spatio_temporal', 'data', 'places_lat_lon_tz_db.tsv'),
            # Path relative to parent directory
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'jyotisha', 'panchaanga', 'spatio_temporal', 'data', 'places_lat_lon_tz_db.tsv'),
            # Absolute path for deployment
            '/opt/render/project/src/jyotisha/panchaanga/spatio_temporal/data/places_lat_lon_tz_db.tsv',
            # Alternative deployment path
            os.path.join(os.getcwd(), '..', 'jyotisha', 'panchaanga', 'spatio_temporal', 'data', 'places_lat_lon_tz_db.tsv')
        ]
        
        tsv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                tsv_path = path
                print(f"Found TSV file at: {tsv_path}")
                break
        
        if not tsv_path:
            print("TSV file not found in any of the expected locations")
            # Return some default places as fallback
            return jsonify({'places': [
                {'name': 'Mumbai', 'sa_name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'tz': '5.5'},
                {'name': 'Delhi', 'sa_name': 'Delhi', 'lat': 28.7041, 'lon': 77.1025, 'tz': '5.5'},
                {'name': 'Chennai', 'sa_name': 'Chennai', 'lat': 13.0827, 'lon': 80.2707, 'tz': '5.5'},
                {'name': 'Kolkata', 'sa_name': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639, 'tz': '5.5'},
                {'name': 'Bangalore', 'sa_name': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946, 'tz': '5.5'},
                {'name': 'Hyderabad', 'sa_name': 'Hyderabad', 'lat': 17.3850, 'lon': 78.4867, 'tz': '5.5'},
                {'name': 'Pune', 'sa_name': 'Pune', 'lat': 18.5204, 'lon': 73.8567, 'tz': '5.5'},
                {'name': 'Ahmedabad', 'sa_name': 'Ahmedabad', 'lat': 23.0225, 'lon': 72.5714, 'tz': '5.5'},
                {'name': 'Jaipur', 'sa_name': 'Jaipur', 'lat': 26.9124, 'lon': 75.7873, 'tz': '5.5'},
                {'name': 'Lucknow', 'sa_name': 'Lucknow', 'lat': 26.8467, 'lon': 80.9462, 'tz': '5.5'}
            ]})

        # Read the TSV file
        with open(tsv_path, encoding='utf-8') as f:
            for i, line in enumerate(f):
                if not line or line.strip() == '':
                    continue  # skip empty lines
                if i == 0:
                    continue  # skip header
                parts = line.strip().split('\t')
                if not isinstance(parts, list) or len(parts) < 5:
                    print(f"Skipping line {i}: parts={parts}")
                    continue
                try:
                    name, sa_name, lat, lon, tz = parts[:5]
                except Exception as e:
                    print(f"Error unpacking line {i}: {parts}, error: {e}")
                    continue
                # Convert DMS to decimal if needed
                def dms_to_decimal(val):
                    if ':' in val:
                        parts = [float(x) for x in val.split(':')]
                        if len(parts) == 3:
                            return parts[0] + parts[1]/60 + parts[2]/3600
                        elif len(parts) == 2:
                            return parts[0] + parts[1]/60
                    return float(val)
                try:
                    lat_f = dms_to_decimal(lat)
                    lon_f = dms_to_decimal(lon)
                except Exception:
                    continue
                places.append({
                    'name': name,
                    'sa_name': sa_name,
                    'lat': lat_f,
                    'lon': lon_f,
                    'tz': tz
                })
        
        print(f"Successfully loaded {len(places)} places from TSV file")
        return jsonify({'places': places})
        
    except Exception as e:
        print(f"Error reading places TSV file: {e}")
        # Return fallback places
        return jsonify({'places': [
            {'name': 'Mumbai', 'sa_name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'tz': '5.5'},
            {'name': 'Delhi', 'sa_name': 'Delhi', 'lat': 28.7041, 'lon': 77.1025, 'tz': '5.5'},
            {'name': 'Chennai', 'sa_name': 'Chennai', 'lat': 13.0827, 'lon': 80.2707, 'tz': '5.5'},
            {'name': 'Kolkata', 'sa_name': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639, 'tz': '5.5'},
            {'name': 'Bangalore', 'sa_name': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946, 'tz': '5.5'},
            {'name': 'Hyderabad', 'sa_name': 'Hyderabad', 'lat': 17.3850, 'lon': 78.4867, 'tz': '5.5'},
            {'name': 'Pune', 'sa_name': 'Pune', 'lat': 18.5204, 'lon': 73.8567, 'tz': '5.5'},
            {'name': 'Ahmedabad', 'sa_name': 'Ahmedabad', 'lat': 23.0225, 'lon': 72.5714, 'tz': '5.5'},
            {'name': 'Jaipur', 'sa_name': 'Jaipur', 'lat': 26.9124, 'lon': 75.7873, 'tz': '5.5'},
            {'name': 'Lucknow', 'sa_name': 'Lucknow', 'lat': 26.8467, 'lon': 80.9462, 'tz': '5.5'}
        ]})

if __name__ == '__main__':
    app.run(debug=True) 